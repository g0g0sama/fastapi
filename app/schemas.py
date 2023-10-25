from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    name: str
    price: int



class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(BaseModel):
    name: str
    price: int
    created_at: datetime

    class Config:
        orm_mode = True