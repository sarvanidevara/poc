from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# Data Model, Validate inputs received from frontend
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

# Data Model, Validate inputs received from frontend in create, update post
class CreatePost(PostBase):
    pass

# Response model (from Backend to frontend)
# Response model (from Backend to frontend)
class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
      orm_mode = True 

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
      orm_mode = True

class PostOut(BaseModel):
    Post: Post    
    votes: int

    class Config:
      orm_mode = True

