from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# from .database import create_db_and_tables
from .routers import post, user, auth, vote


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_db_and_tables()
    # print('DB tables created')
    yield
    print('App shutting down')

app = FastAPI(lifespan=lifespan)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message': 'Hello Ting Ting'}

