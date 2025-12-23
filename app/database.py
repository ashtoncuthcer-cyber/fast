from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = 'postgresql+psycopg://postgres:password@127.0.0.1:5432/fastapi'

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]