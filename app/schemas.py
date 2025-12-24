from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime