from pydantic import BaseModel, EmailStr
from datetime import datetime

    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    created_at: datetime

    class Config:
     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
     orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str





