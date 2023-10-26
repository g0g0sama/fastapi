from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    name: str
    price: int
    



class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
    