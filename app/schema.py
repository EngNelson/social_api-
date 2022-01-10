from os import access
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

    
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

class Token(BaseException):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None





