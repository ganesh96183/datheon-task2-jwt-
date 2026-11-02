# Datheon Task 2 - JWT Authentication

## Project Overview
A FastAPI application demonstrating user registration,
password hashing, JWT authentication, and role-based
access control (RBAC).

## Features
- User registration
- Password hashing using bcrypt
- Login with JWT access tokens
- Protected user profile endpoint
- Admin-only endpoint
- Interactive API documentation with Swagger UI

## Technologies
- Python
- FastAPI
- Uvicorn
- JWT
- Passlib and bcrypt

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the server:

```bash
python -m uvicorn main:app --reload
```

Open Swagger UI:

http://127.0.0.1:8000/docs

## Note
This is a learning project. User data is stored in
memory and is lost when the server restarts.
Use persistent storage and secure secret management
before production deployment.
