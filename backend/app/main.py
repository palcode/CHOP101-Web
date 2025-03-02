from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import uuid
import logging

from .core.config import settings
from .core.security import create_access_token, verify_google_token
from .api.deps import get_current_user
from . import models, schemas
from .database import engine, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/google")
async def google_auth(request: schemas.GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        # Verify the token
        idinfo = verify_google_token(request.credential)
        logger.info(f"Google token verified for email: {idinfo['email']}")

        # Check if user exists
        user = db.query(models.User).filter(models.User.email == idinfo["email"]).first()
        
        if not user:
            logger.info(f"Creating new user for email: {idinfo['email']}")
            # Create new user
            user = models.User(
                id=str(uuid.uuid4()),
                email=idinfo["email"],
                name=idinfo["name"],
                picture=idinfo.get("picture", ""),
                is_active=True
            )
            db.add(user)
            
            # Create user profile
            profile = models.UserProfile(
                id=str(uuid.uuid4()),
                user_id=user.id
            )
            db.add(profile)
            db.commit()
            db.refresh(user)
            db.refresh(profile)
            logger.info(f"Created new user and profile for {user.email}")
        else:
            logger.info(f"Existing user found: {user.email}")
            # Ensure profile exists for existing user
            if not user.profile:
                logger.info(f"Creating missing profile for existing user: {user.email}")
                profile = models.UserProfile(
                    id=str(uuid.uuid4()),
                    user_id=user.id
                )
                db.add(profile)
                db.commit()
                db.refresh(user)
            else:
                logger.info(f"Using existing profile for user: {user.email}")
                profile = user.profile

        # Generate access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at = datetime.utcnow() + access_token_expires
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        logger.info(f"Generated access token for user: {user.email}")

        # Create or update session
        session = models.Session(
            id=str(uuid.uuid4()),
            user_id=user.id,
            token=access_token,
            expires_at=expires_at
        )
        db.add(session)
        db.commit()
        logger.info(f"Created new session for user: {user.email}")

        # Ensure we have the latest user data
        db.refresh(user)
        
        # Log the response data
        response_data = {
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "picture": user.picture,
                "is_active": user.is_active,
                "profile": {
                    "id": user.profile.id if user.profile else None,
                    "address": user.profile.address if user.profile else None,
                    "phone": user.profile.phone if user.profile else None,
                    "bio": user.profile.bio if user.profile else None
                } if user.profile else None
            }
        }
        logger.info(f"Returning response data for user {user.email}: {response_data}")
        return response_data

    except Exception as e:
        logger.error(f"Error in google_auth: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching user data for: {current_user.email}")
    # Ensure profile exists
    if not current_user.profile:
        logger.info(f"Creating missing profile for user: {current_user.email}")
        profile = models.UserProfile(
            id=str(uuid.uuid4()),
            user_id=current_user.id
        )
        db.add(profile)
        db.commit()
        db.refresh(current_user)
    
    # Log the response data
    logger.info(f"User data: {current_user.email}, Profile: {current_user.profile.__dict__ if current_user.profile else None}")
    return current_user

@app.put("/users/me", response_model=schemas.User)
async def update_user_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@app.get("/users/me/profile", response_model=schemas.UserProfile)
async def read_user_profile(current_user: models.User = Depends(get_current_user)):
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return current_user.profile

@app.put("/users/me/profile", response_model=schemas.UserProfile)
async def update_user_profile(
    profile_update: schemas.UserProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating profile for user: {current_user.email}")
    logger.info(f"Update data: {profile_update.dict()}")
    
    profile = current_user.profile
    if not profile:
        logger.info(f"Creating new profile for user: {current_user.email}")
        profile = models.UserProfile(
            id=str(uuid.uuid4()),
            user_id=current_user.id
        )
        db.add(profile)
        current_user.profile = profile
    
    # Update profile fields
    for key, value in profile_update.dict(exclude_unset=True).items():
        logger.info(f"Setting {key} = {value}")
        setattr(profile, key, value)
    
    try:
        db.commit()
        db.refresh(profile)
        logger.info(f"Profile updated successfully: {profile.__dict__}")
        return profile
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update profile") 