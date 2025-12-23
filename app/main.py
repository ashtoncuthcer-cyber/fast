import time
from fastapi import FastAPI, HTTPException, Response, status
from psycopg.rows import dict_row
import psycopg
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg.connect(
            host='localhost',
            dbname='fastapi',
            user='postgres',
            password='password',
        )
        cursor = conn.cursor(row_factory=dict_row)
        print('DB connected')
        break
    except Exception as error:
        print('Connecting to db failed')
        print('Error: ', error)

@app.get('/')
def root():
    return {'message': 'Hello Ting Ting'}

@app.get('/posts')
def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()

    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        '''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
        (post.title, post.content, post.published)
    )
    post = cursor.fetchone()
    conn.commit()
    return {'data': post}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute(
        '''SELECT * FROM posts WHERE id = %s''',
        (str(id), )
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    return {'data': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        '''DELETE FROM posts WHERE id = %s RETURNING *''',
        (str(id), ),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(
        '''UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *''',
        (post.title, post.content, post.published, str(id)),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found',
        )
    conn.commit()
    return {'data': post}