from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User
from schemas import UserCreate, UserLogin, UserResponse, Token
from auth import hash_password, authenticate_user, create_access_token
from deps import get_current_user
from routes.vault import router as vault_router
from routes.nominee import router as nominee_router
from routes.access import router as access_router
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

app = FastAPI()

# CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(vault_router)
app.include_router(nominee_router)
app.include_router(access_router)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# Register
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login
@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": authenticated_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Google OAuth Login
class GoogleToken(BaseModel):
    credential: str = ""
    email: str = ""

@app.post("/auth/google", response_model=Token)
def google_login(payload: GoogleToken, db: Session = Depends(get_db)):
    email = None

    # Flow 1: ID token from GoogleLogin component
    if payload.credential:
        try:
            idinfo = id_token.verify_oauth2_token(
                payload.credential,
                google_requests.Request(),
                GOOGLE_CLIENT_ID
            )
            email = idinfo.get("email")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid Google token")

    # Flow 2: Email from useGoogleLogin + userinfo API
    if not email and payload.email:
        email = payload.email

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Google token")

    # Find or create user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            password_hash="GOOGLE_OAUTH_USER"  # no password needed for Google users
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route example
@app.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user