
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlmodel import select


from .. import models, schemas, oauth2
from ..database import  SessionDep

router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get('/', response_model=List[schemas.Post])
def get_posts(
    db: SessionDep, 
    user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ''
):
    posts = db.exec(
        select(models.Post)
        .where(models.Post.owner_id == user.id)
        .where(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    ).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreateUpdate, db: SessionDep, user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post   

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: SessionDep, user: models.User = Depends(oauth2.get_current_user)):
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep, user: models.User = Depends(oauth2.get_current_user)):
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized',
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreateUpdate, db: SessionDep, user: models.User = Depends(oauth2.get_current_user)):
    db_post = db.exec(select(models.Post).where(models.Post.id == id)).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    if db_post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized',
        )
    post_data = post.model_dump()
    for key, value in post_data.items():
        setattr(db_post, key, value)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

