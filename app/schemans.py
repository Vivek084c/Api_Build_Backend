from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint 
# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool=True
#     # rating:Optional[int]=None
    
# class CreatePost(BaseModel):
#     title:str
#     content:str
#     published: bool=True
    
# class UpdatePost(BaseModel):
#     title:str
#     content:str
#     published: bool
    
class PostBase(BaseModel):
    title:str
    content:str
    published: bool=True
    
class PostCreate(PostBase):
    owner_id:int
    pass

#below class is used to define the response schema for api

# class Post(BaseModel):
#     id:int
#     title:str
#     content:str
#     published:bool
#     created_at:datetime
#     class Config:
#         orm_mode=True
        
        #OR we can define it as follow 
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True
        
class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    class Config:
        orm_mode=True
        
class PostOut(PostBase):
    Post:Post
    votes:int
    class Config:
        orm_mode=True
    
#schemans for handling users
class UserCreate(BaseModel):
    email:EmailStr
    password:str    
    

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]=None
    
class Vote(BaseModel):
    post_id:int
    dir: int



    