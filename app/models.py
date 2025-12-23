from datetime import datetime 
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, text, TIMESTAMP

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
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text('now()'),
        )
    )
