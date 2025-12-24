from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, Response, status

from sqlmodel import select

from . import models, schemas
from .database import create_db_and_tables, SessionDep




@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print('DB tables created')
    yield
    print('App shutting down')

app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    return {'message': 'Hello Ting Ting'}


@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: SessionDep):
    posts = db.exec(select(models.Post)).all()
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreateUpdate, db: SessionDep):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: SessionDep):
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep):
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreateUpdate, db: SessionDep):
    db_post = db.exec(select(models.Post).where(models.Post.id == id)).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    post_data = post.model_dump()
    for key, value in post_data.items():
        setattr(db_post, key, value)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post