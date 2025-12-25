from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlmodel import select

from .. import models, schemas, utils, oauth2
from ..database import  SessionDep

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(db: SessionDep, user_data: OAuth2PasswordRequestForm = Depends()):
    user = db.exec(select(models.User).where(models.User.email == user_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credential',
        )
    if not utils.verify(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credential',
        )
    ## still developing
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }