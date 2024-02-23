from fastapi import FastAPI
from fastapi.params import Body
from fastapi import Response,HTTPException,status,Depends

from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from .routers import post,user,auth



#builing the model
from sqlalchemy.orm import Session
from . import models,schemans,utils
from .database import engine,get_db
models.Base.metadata.create_all(bind=engine)
 #setting the dependencies



app=FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

    
#connecting to postgrace database
while True:
    try:
        conn=psycopg2.connect(host="localhost",database="FastApi",user='postgres',password='vivek123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection established")
        break
    except Exception as error:
        print(f"the connection to database failed error: {error}")
        time.sleep(2)
        
#list to handel dataset in memory
my_post=[
    {"title":"this is the title of post", "content":"this is the content","id":1},
    {"title":"my favourite foood","content":"my favourite food is pizza","id":2}
]

def find_post(id):
    for p in my_post:
        if p["id"]==id:
            return p

def find_post_index(id):
    for i,p in enumerate (my_post):
        if p["id"]==id:
            return i

@app.get("/")
async def root():
    return {f"hellow world: welcome to my api by vivek chaudahry"}



@app.get('/sqlalchemy')
def test_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts

