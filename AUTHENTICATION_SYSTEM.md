# Authentication System Documentation

## Overview
This document describes the complete authentication system implemented for the Physical AI & Humanoid Robotics project. The system includes both backend and frontend components to provide secure user registration, login, and protected resource access.

## Backend Implementation

### Technologies Used
- **FastAPI**: Web framework for building the API
- **SQLModel**: ORM for database operations (combines SQLAlchemy and Pydantic)
- **PostgreSQL**: Database for user storage (Neon serverless)
- **Passlib**: Password hashing
- **PyJWT**: JSON Web Token generation and verification
- **BCrypt**: Password hashing algorithm

### Database Models
- **User Model**: Stores user information including email, name, hashed password, and status flags
- **Database Schema**: Uses UUID for user IDs, with indexes on email for efficient lookups

### API Endpoints
- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Authenticate user and return JWT token
- `POST /api/auth/logout`: Logout user (client-side token removal)
- `GET /api/auth/me`: Get current user profile
- `PUT /api/auth/me`: Update user profile

### Security Features
- Passwords are hashed using BCrypt with automatic salting
- JWT tokens with configurable expiration (default 30 minutes)
- Protected routes using Bearer token authentication
- Input validation using Pydantic models

## Frontend Implementation

### Technologies Used
- **React**: Component-based UI framework
- **Docusaurus**: Static site generator
- **React Context API**: State management for authentication
- **Custom Hooks**: Reusable authentication logic

### Components
- **AuthContext**: Global authentication state management
- **LoginForm**: User login form with validation
- **RegisterForm**: User registration form with validation
- **UserProfile**: Display and edit user profile information
- **ProtectedRoute**: Component wrapper for protected content

### Hooks
- `useAuth`: Access authentication state and methods
- `useLogin`: Handle login logic with loading and error states
- `useRegister`: Handle registration logic with loading and error states
- `useLogout`: Handle logout functionality
- `useAuthStatus`: Check authentication status

### Features
- Persistent login using localStorage
- Protected route rendering
- Profile editing capability
- Session management

## Environment Variables

### Backend
The following environment variables are required for the authentication system:

```
# Database Configuration
DB_USER=neondb_owner
DB_PASSWORD=your_db_password
DB_HOST=ep-xxx.us-east-1.aws.neon.tech
DB_PORT=5432
DB_NAME=neondb

# API Configuration
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

## Implementation Details

### Password Security
- Passwords are never stored in plain text
- All passwords are hashed using BCrypt with a cost factor of 12
- Automatic salting prevents rainbow table attacks

### Token Management
- JWT tokens are generated upon successful login
- Tokens expire after 30 minutes by default
- Tokens are stored in browser localStorage
- Tokens are sent in Authorization header as Bearer tokens

### Error Handling
- Comprehensive error handling for all authentication operations
- User-friendly error messages
- Proper HTTP status codes for different error conditions

## Usage

### Registration
1. User provides email, password, and name
2. System validates input
3. Password is hashed
4. User is stored in database
5. User is automatically logged in

### Login
1. User provides email and password
2. System verifies credentials against database
3. JWT token is generated and returned
4. Token is stored in localStorage

### Protected Routes
1. Components wrapped with ProtectedRoute
2. Authentication status is checked
3. If not authenticated, fallback content is shown
4. If authenticated, protected content is rendered

## Testing

The system includes test scripts to verify functionality:
- `test_auth.py`: Pytest-based tests
- `test_auth_requests.py`: Manual test script using requests library

## Security Considerations

### Implemented
- Password hashing with BCrypt
- JWT token authentication
- Input validation
- Secure token storage

### Recommendations for Production
- Implement rate limiting for authentication endpoints
- Add multi-factor authentication
- Implement secure token refresh mechanism
- Add CSRF protection
- Use HTTPS in production
- Regular security audits

## Future Enhancements

- Social authentication (Google, GitHub, etc.)
- Password reset functionality
- Email verification
- Role-based access control
- Session management improvements
- Audit logging

## File Structure

```
backend/
├── src/
│   ├── api/
│   │   └── auth.py                 # Authentication API endpoints
│   ├── models/
│   │   └── user.py                 # User model definitions
│   ├── services/
│   │   └── auth_service.py         # Authentication business logic
│   ├── database/
│   │   ├── database.py             # Database connection and models
│   │   └── migrations/             # Database migration files
│   └── core/
│       └── config.py               # Configuration including DB settings
└── requirements.txt                # Dependencies including auth libraries

frontend/
├── src/
│   ├── contexts/
│   │   └── AuthContext.tsx         # Authentication context
│   ├── hooks/
│   │   └── useAuth.ts              # Authentication hooks
│   ├── components/
│   │   └── Auth/
│   │       ├── LoginForm.tsx       # Login form component
│   │       ├── RegisterForm.tsx    # Registration form component
│   │       ├── ProtectedRoute.tsx  # Protected route component
│   │       └── UserProfile.tsx     # User profile component
│   ├── pages/
│   │   ├── login.tsx               # Login page
│   │   ├── register.tsx            # Registration page
│   │   └── profile.tsx             # User profile page
│   └── theme/
│       └── Layout/                 # Theme wrapper with auth provider
```

## Dependencies

### Backend
- `passlib[bcrypt]`: Password hashing
- `python-jose[cryptography]`: JWT handling
- `sqlmodel`: ORM (combines SQLAlchemy and Pydantic)
- `asyncpg`: PostgreSQL driver

### Frontend
- React Context API
- React Hooks
- TypeScript type safety

This authentication system provides a secure and scalable foundation for user management in the Physical AI & Humanoid Robotics project.