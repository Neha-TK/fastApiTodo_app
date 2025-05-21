from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas import UserCreate, Token
from app.db.models import User
from app.helper.auth import hash_password, verify_password, create_access_token
from app.api.deps import get_db

router = APIRouter()

@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == user_data.username)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user_data.username, password=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}