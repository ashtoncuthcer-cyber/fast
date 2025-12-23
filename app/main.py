from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from sqlmodel import select

from . import models
from .database import create_db_and_tables, SessionDep


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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


@app.get('/posts')
def get_posts(db: SessionDep):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    posts = db.exec(select(models.Post)).all()
    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: SessionDep):
    # cursor.execute(
    #     '''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
    #     (post.title, post.content, post.published)
    # )
    # post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}

@app.get('/posts/{id}')
def get_post(id: int, db: SessionDep):
    # cursor.execute(
    #     '''SELECT * FROM posts WHERE id = %s''',
    #     (str(id), )
    # )
    # post = cursor.fetchone()
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    return {'data': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep):
    # cursor.execute(
    #     '''DELETE FROM posts WHERE id = %s RETURNING *''',
    #     (str(id), ),
    # )
    # post = cursor.fetchone()
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    # conn.commit()
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post, db: SessionDep):
    # cursor.execute(
    #     '''UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *''',
    #     (post.title, post.content, post.published, str(id)),
    # )
    # post = cursor.fetchone()
    db_post = db.exec(select(models.Post).where(models.Post.id == id)).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    post_data = post.model_dump()
    for key, value in post_data.items():
        setattr(db_post, key, value)
    # conn.commit()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return {'data': db_post}