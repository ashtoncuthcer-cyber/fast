from fastapi import APIRouter, HTTPException, status

from sqlmodel import select

from .. import models, schemas, utils
from ..database import  SessionDep

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_data: schemas.UserLogin, db: SessionDep):
    user = db.exec(select(models.User).where(models.User.email == user_data.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credential',
        )
    if not utils.verify(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credential',
        )
    ## still developing
    return {'token': 'example token'}