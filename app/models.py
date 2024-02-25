from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql.expression import text
#creating table for postgrace
class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False) 
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #creating a column for foreign key
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    #defining a relatioship to retrive the email id based on the owner_id , we have to mention the class i.e User and not the table i.e is the users
    owner=relationship("User")
    
#creating table for handling user accounts
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
#creating table for liking and dislikeing a post 
class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)



