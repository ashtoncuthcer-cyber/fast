from fastapi import APIRouter, HTTPException, status

from sqlmodel import select

from .. import models, schemas, utils
from ..database import  SessionDep

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: SessionDep):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: SessionDep):
    user = db.exec(select(models.User).where(models.User.id == id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with id: {id} not found',
        )
    return user
