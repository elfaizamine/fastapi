from pydantic import BaseModel, EmailStr
from datetime import datetime



class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published: bool = True
    class Config:
        from_attributes=True



class UserCreate(BaseModel):
    email: EmailStr
    password:str



class UserResponse(BaseModel):
    id:int
    email: EmailStr
    class Config:
        from_attributes=True




    







