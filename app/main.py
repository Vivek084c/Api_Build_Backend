from fastapi import FastAPI
from fastapi.params import Body
from fastapi import Response,HTTPException,status,Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

#builing the model
from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db
models.Base.metadata.create_all(bind=engine)
 #setting the dependencies



app=FastAPI()

class Post(BaseModel):
    title:str
    contents:str
    published: bool=True
    rating:Optional[int]=None
    
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

@app.get("/posts")
def get_posts_data():
    #executing a query to postgrace database
    cursor.execute(""" SELECT * FROM posts""")
    post=cursor.fetchall()
    # print(post)
    # return {"data":my_post}
    return {"data":post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    # print(new_post.rating)
    # post_dict=new_post.dict()
    # post_dict["id"]=randrange(0,100000)
    # my_post.append(post_dict)
    cursor.execute(""" INSERT INTO posts (title,contents,published) VALUES (%s, %s, %s) RETURNING *""",
                   (new_post.title,new_post.contents,new_post.published))
    conn.commit()
    newPosts=cursor.fetchone()
    return {"data:":newPosts}


# title- str and content- str 
#if we want specific content from the user, we can use pydantic for it- to this we define a class 

#requesst to get a specific post
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s""" , (str(id),))
    test_post=cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} is not found")
    return {"post_details":test_post}
    # print(id)
    # post=find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"the post with the id {id} is not found")
    # return {"post_details":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleate_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s returning*""",(str(id),))
    deleated_post=cursor.fetchone()
    conn.commit()
    #deleating the post 
    # index=find_post_index(id)
    if deleated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} is not found")
    # my_post.pop(deleated_post)
    # return {"message":"post was successfully deleted"}
    # we dont send any data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title=%s , contents=%s , published=%s WHERE id=%s""",
                   (post.title,post.contents,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    # print(post)
    
    # index=find_post_index(id)
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} is not found")
        
    # post_dict=post.dict()
    # post_dict["id"]=id
    # my_post[index]=post_dict
    return {"data":updated_post}