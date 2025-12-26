from datetime import datetime
from typing import List 
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, ForeignKey, text, TIMESTAMP

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(
        default=True, 
        sa_column_kwargs={'server_default': text('TRUE')}
    )
    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('now()'),
        )
    )
    owner_id: int = Field(
        sa_column=Column(
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
        )
    )
    owner: 'User' = Relationship(back_populates='posts')

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('now()'),
        )
    )
    posts: List['Post'] = Relationship(back_populates='owner') 