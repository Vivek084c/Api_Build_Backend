from pydantic import BaseModel
from datetime import datetime

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
class Post(PostBase):
    id:int
    created_at:datetime
    class Config:
        orm_mode=True
    