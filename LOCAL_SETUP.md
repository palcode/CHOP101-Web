# Local Development Setup Guide

This guide will help you set up the development environment on your local machine.

## Prerequisites Installation

### 1. Python Setup
```bash
# For macOS (using Homebrew)
brew install python@3.11

# For Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. Node.js Setup
```bash
# For macOS (using Homebrew)
brew install node@18

# For Ubuntu/Debian (using nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

### 3. PostgreSQL Setup
```bash
# For macOS (using Homebrew)
brew install postgresql@15
brew services start postgresql@15

# For Ubuntu/Debian
sudo apt install postgresql-15
sudo systemctl start postgresql
```

### 4. Docker Setup (Optional, for containerized development)
```bash
# For macOS
brew install docker docker-compose

# For Ubuntu/Debian
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker $USER  # Log out and back in after this
```

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the Google OAuth API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google OAuth2 API"
   - Click "Enable"
4. Configure OAuth consent screen:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in application name and user support email
   - Add authorized domains
   - Save and continue
5. Create OAuth credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URIs:
     ```
     http://localhost:3000
     http://localhost:8000/auth/google/callback
     ```
   - Save the Client ID and Client Secret

## Local Environment Setup

### 1. Clone and Setup Project
```bash
# Clone repository
git clone <repository-url>
cd user-management-microservice

# Create local environment file
cp .env.example .env
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create local PostgreSQL database
psql -U postgres
CREATE DATABASE userdb;
\q

# Update .env with database credentials
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/userdb
```

### 3. Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Update .env with API URL
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application Locally

### 1. Start Backend Server
```bash
# In backend directory with virtual environment activated
uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend Development Server
```bash
# In frontend directory
npm start
```

## Running Tests

### Backend Tests
```bash
# In backend directory
pytest                 # Run all tests
pytest --cov=app      # Run tests with coverage
pytest -v             # Run tests with verbose output
```

### Frontend Tests
```bash
# In frontend directory
npm test              # Run tests
npm test -- --coverage  # Run tests with coverage
```

## Common Issues and Solutions

### 1. Database Connection Issues
```bash
# Check PostgreSQL service status
sudo systemctl status postgresql

# Reset PostgreSQL password
sudo -u postgres psql
\password postgres
```

### 2. Port Conflicts
```bash
# Check if ports are in use
lsof -i :8000  # Check backend port
lsof -i :3000  # Check frontend port

# Kill process using port
kill -9 <PID>
```

### 3. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Node.js Dependencies Issues
```bash
# Clear npm cache
npm cache clean --force

# Remove and reinstall node_modules
rm -rf node_modules package-lock.json
npm install
```

## Development Tools (Recommended)

1. **VS Code Extensions**:
   - Python
   - Pylance
   - ESLint
   - Prettier
   - Docker
   - GitLens

2. **API Testing Tools**:
   - Postman or Insomnia
   - FastAPI Swagger UI (http://localhost:8000/docs)

3. **Database Tools**:
   - pgAdmin or DBeaver for PostgreSQL management

## Environment Variables

Create a `.env` file in the root directory with these variables:
```bash
# Backend
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/userdb
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
JWT_SECRET_KEY=your_secure_jwt_key
CORS_ORIGINS=http://localhost:3000

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your_client_id
```

## Code Style and Linting

### Backend
```bash
# Install development dependencies
pip install black flake8 isort

# Run formatters
black .
isort .

# Run linter
flake8
```

### Frontend
```bash
# Run ESLint
npm run lint

# Run Prettier
npm run format
``` 