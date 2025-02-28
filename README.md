# User Management Microservice

A modern, secure, and scalable user management system built with FastAPI and React. This system serves as the foundation for an e-commerce application, handling user authentication, profile management, and address information.

## 🚀 Features

### Backend
- FastAPI-based RESTful API
- PostgreSQL database with SQLAlchemy ORM
- Google OAuth2 authentication
- JWT token-based authentication
- Input validation with Pydantic
- Rate limiting and security headers
- Comprehensive error handling
- Logging system
- Docker containerization

### Frontend
- React with Material-UI components
- Google OAuth integration
- Redux state management
- Form validation with Formik and Yup
- Responsive design
- Error handling with toast notifications
- Protected routes
- API error interceptors

## 🛠️ Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Google OAuth credentials
- Git

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd user-management-microservice
```

2. Set up Google OAuth credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one
   - Enable Google OAuth API
   - Create credentials (OAuth 2.0 Client ID)
   - Add authorized redirect URIs:
     - http://localhost:3000
     - http://localhost:8000/auth/google/callback

3. Create `.env` file in the root directory:
```bash
# Backend
DATABASE_URL=postgresql://postgres:postgres@db:5432/userdb
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
JWT_SECRET_KEY=your-secure-jwt-key
CORS_ORIGINS=http://localhost:3000

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

## 🚀 Running the Application

### Using Docker (Recommended)

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs
   - Alternative API Documentation: http://localhost:8000/api/redoc

### Local Development

#### Backend

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

#### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## 🧪 Testing

### Backend Tests

1. Run the test suite:
```bash
# In the backend directory
pytest

# With coverage report
pytest --cov=app

# With verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py
```

2. Run integration tests:
```bash
pytest tests/test_integration.py
```

### Frontend Tests

1. Run the test suite:
```bash
# In the frontend directory
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Rate limiting
- CORS protection
- SQL injection protection
- XSS protection headers
- CSRF protection
- Input validation
- Error handling
- Secure headers

## 📝 API Documentation

### Authentication Endpoints
- `POST /auth/google` - Google OAuth authentication
- `POST /auth/refresh` - Refresh JWT token

### User Endpoints
- `POST /users/` - Create a new user
- `GET /users/` - List all users (with pagination and filters)
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

## 🔍 Monitoring and Logging

- Application logs are stored in `app.log`
- Rotating file handler with 5 backup files
- Log format: `timestamp - name - level - message`
- Rate limiting logs
- Error tracking
- Request/Response logging

## 🚀 Deployment

1. Update environment variables for production:
```bash
# Update CORS_ORIGINS
CORS_ORIGINS=https://your-production-domain.com

# Update API URL
REACT_APP_API_URL=https://api.your-production-domain.com
```

2. Build production Docker images:
```bash
docker-compose -f docker-compose.prod.yml build
```

3. Deploy containers:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🔄 Future Extensions

This microservice is designed to be part of a larger e-commerce application. Future extensions include:

- Product catalog integration
- Shopping cart functionality
- Order management
- Payment processing
- Shipping integration
- Inventory management
- Analytics and reporting

## 🐛 Troubleshooting

1. Database connection issues:
```bash
# Check database logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up --build
```

2. Frontend connection issues:
```bash
# Check API URL in .env
# Clear browser cache and local storage
# Check CORS settings
```

3. Google OAuth issues:
```bash
# Verify credentials in .env
# Check authorized redirect URIs
# Ensure Google OAuth API is enabled
```

## 📚 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.