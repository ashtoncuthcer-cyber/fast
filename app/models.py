from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True
