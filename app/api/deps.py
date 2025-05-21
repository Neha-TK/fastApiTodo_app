from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from app.db.engine import engine
from app.db.models import User
from app.helper.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    with Session(engine) as session:
        yield session

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user
