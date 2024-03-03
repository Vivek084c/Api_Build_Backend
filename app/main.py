from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from typing import List
from random import randrange
from .routers import post,user,auth, vote
from .config import settings

#builing the model
import psycopg2
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db
models.Base.metadata.create_all(bind=engine)
 #setting the dependencies



app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#connecting to postgrace database
while True:
    try:
        conn=psycopg2.connect(host="localhost",database="FastApi",user='postgres',password='vivek123')
        cursor=conn.cursor()
        print("Database connection established")
        break
    except Exception as error:
        print(f"the connection to database failed error: {error}")
        time.sleep(2)
        
# #list to handel dataset in memory
# my_post=[
#     {"title":"this is the title of post", "content":"this is the content","id":1},
#     {"title":"my favourite foood","content":"my favourite food is pizza","id":2}
# ]

# def find_post(id):
#     for p in my_post:
#         if p["id"]==id:
#             return p

# def find_post_index(id):
#     for i,p in enumerate (my_post):
#         if p["id"]==id:
#             return i

# @app.get("/")
# async def root():
#     return {f"hellow world: welcome to my api by vivek chaudahry"}



# @app.get('/sqlalchemy')
# def test_posts(db:Session=Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return posts

