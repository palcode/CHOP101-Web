# Docker Setup Guide

This guide explains how to run the application using Docker for local development.

## Prerequisites

1. **Install Docker**:
   ```bash
   # For macOS
   brew install docker docker-compose

   # For Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo systemctl start docker
   sudo usermod -aG docker $USER  # Add user to docker group
   # Log out and log back in for group changes to take effect
   ```

2. **Install Google Cloud SDK** (for OAuth setup):
   ```bash
   # For macOS
   brew install google-cloud-sdk

   # For Ubuntu/Debian
   sudo apt-get install apt-transport-https ca-certificates gnupg
   echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
   curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
   sudo apt-get update && sudo apt-get install google-cloud-sdk
   ```

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google OAuth API
4. Configure OAuth consent screen
5. Create OAuth 2.0 credentials
6. Add authorized redirect URIs:
   ```
   http://localhost:3000
   http://localhost:8000/auth/google/callback
   ```

## Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd user-management-microservice
   ```

2. **Create environment files**:

   Create `.env` file in the root directory:
   ```bash
   # Database
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=userdb
   DATABASE_URL=postgresql://postgres:postgres@db:5432/userdb

   # Backend
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   JWT_SECRET_KEY=your_jwt_secret
   CORS_ORIGINS=http://localhost:3000

   # Frontend
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
   ```

## Running the Application

1. **Build and start containers**:
   ```bash
   # Build images
   docker-compose build

   # Start services
   docker-compose up
   ```

2. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs
   - PostgreSQL: localhost:5432

## Development Workflow

1. **View logs**:
   ```bash
   # View all logs
   docker-compose logs -f

   # View specific service logs
   docker-compose logs -f api
   docker-compose logs -f frontend
   docker-compose logs -f db
   ```

2. **Rebuild specific services**:
   ```bash
   # Rebuild and restart API
   docker-compose up -d --build api

   # Rebuild and restart frontend
   docker-compose up -d --build frontend
   ```

3. **Execute commands in containers**:
   ```bash
   # Run backend tests
   docker-compose exec api pytest

   # Run frontend tests
   docker-compose exec frontend npm test

   # Access database
   docker-compose exec db psql -U postgres
   ```

## Common Docker Operations

1. **Container Management**:
   ```bash
   # Stop containers
   docker-compose down

   # Remove volumes (will delete database data)
   docker-compose down -v

   # Remove all containers and images
   docker-compose down --rmi all
   ```

2. **Troubleshooting**:
   ```bash
   # Check container status
   docker-compose ps

   # Check container resources
   docker stats

   # View container logs
   docker-compose logs -f [service_name]
   ```

3. **Database Operations**:
   ```bash
   # Backup database
   docker-compose exec db pg_dump -U postgres userdb > backup.sql

   # Restore database
   docker-compose exec -T db psql -U postgres userdb < backup.sql
   ```

## Development Tips

1. **Hot Reloading**:
   - Backend code changes will automatically reload
   - Frontend changes will trigger automatic rebuilds

2. **Volume Mounts**:
   - Source code is mounted as volumes
   - Changes in your IDE reflect immediately
   - Node modules are in a named volume for performance

3. **Database Persistence**:
   - PostgreSQL data is persisted in a named volume
   - Survives container restarts
   - Can be backed up and restored

## Common Issues and Solutions

1. **Permission Issues**:
   ```bash
   # Fix docker permission issues
   sudo chown -R $USER:$USER .
   ```

2. **Port Conflicts**:
   ```bash
   # Check ports in use
   sudo lsof -i :3000
   sudo lsof -i :8000
   sudo lsof -i :5432
   ```

3. **Container Issues**:
   ```bash
   # Reset all containers and volumes
   docker-compose down -v
   docker-compose up --build
   ```

4. **Cache Issues**:
   ```bash
   # Clear Docker build cache
   docker builder prune

   # Force rebuild without cache
   docker-compose build --no-cache
   ```

## Production Considerations

1. **Security**:
   - Change default passwords
   - Use secure JWT secret
   - Enable HTTPS
   - Configure CORS properly

2. **Performance**:
   - Use production builds
   - Enable caching
   - Configure proper resource limits

3. **Monitoring**:
   - Set up logging
   - Configure health checks
   - Monitor resource usage 

4. Generate a secure random key (you can use any of these methods):

# Method 1: Using openssl (recommended)
openssl rand -base64 32

# Method 2: Using python
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'

# Method 3: Using node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'));" 