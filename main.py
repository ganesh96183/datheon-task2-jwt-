from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


app = FastAPI(title="Datheon Task 2 - JWT Authentication")

# JWT configuration: development example only
SECRET_KEY = token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Temporary storage for learning purposes.
# Users disappear when the server restarts.
fake_users_db = {}


class UserRegister(BaseModel):
    username: str
    password: str


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(username: str, role: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expires
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/")
def home():
    return {"message": "Datheon JWT Authentication API is running"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password),
        "role": "user"
    }

    return {"message": "User registered successfully"}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form.username)

    if not user or not verify_password(
        form.password, user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(
        user["username"], user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if not username:
            raise credentials_error

    except JWTError:
        raise credentials_error

    user = fake_users_db.get(username)

    if not user:
        raise credentials_error

    return user


@app.get("/users/me")
def read_my_profile(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "role": user["role"]
    }


@app.get("/admin")
def admin_only(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return {"message": "Welcome, admin!"}