from contextlib import asynccontextmanager
from fastapi import FastAPI


from .database import create_db_and_tables
from .routers import post, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print('DB tables created')
    yield
    print('App shutting down')

app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {'message': 'Hello Ting Ting'}

