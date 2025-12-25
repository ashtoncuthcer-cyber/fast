#app/oauth2.py
#openssl rand -hex 32

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError
from sqlmodel import select

from .database import SessionDep
from . import schemas, models

SECRET_KEY = "14756bcfaa418006ed1ef1cad092bef5e6b84d5ec8aefbce7fdd26d0986e8046"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 4

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get('user_id'))
        if not user_id: raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception
    return user_id

def get_current_user(db: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    user_id =  verify_access_token(token, credentials_exception)
    user = db.exec(select(models.User).where(models.User.id == user_id)).first()
    return user