from .. import models,schemans,utils
from fastapi import Response,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import List

router=APIRouter(
    prefix="/posts",tags=["posts"]
)

@router.get("/",response_model=List[schemans.Post])
def get_posts_data(db:Session=Depends(get_db)):
    
    #executing a query to postgrace database
    # print(post)
    # return {"data":my_post}
    
    # cursor.execute(""" SELECT * FROM posts""")
    # post=cursor.fetchall()
    
    posts=db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemans.Post)
def create_post(new_post: schemans.PostCreate, db:Session=Depends(get_db)):
    
    # print(new_post.rating)
    # post_dict=new_post.dict()
    # post_dict["id"]=randrange(0,100000)
    # my_post.append(post_dict)
    
    # cursor.execute(""" INSERT INTO posts (title,contents,published) VALUES (%s, %s, %s) RETURNING *""",
    #                (new_post.title,new_post.contents,new_post.published))
    # conn.commit()
    # newPosts=cursor.fetchone()
    
    #IMP: if instead of 4 columsn we had 50 columns then it would be ineffecitent to do it as it will be a long line 
   
    # newPosts=models.Post(title=new_post.title, content=new_post.contents, published=new_post.published)
    #OR
    newPosts=models.Post(**new_post.dict())
    db.add(newPosts)
    db.commit()
    db.refresh(newPosts)
    
    return newPosts


# title- str and content- str 
#if we want specific content from the user, we can use pydantic for it- to this we define a class 

#requesst to get a specific post
@router.get("/{id}",response_model=schemans.Post)
def get_post(id:int, db:Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s""" , (str(id),))
    # test_post=cursor.fetchone()
    

    # print(id)
    # post=find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"the post with the id {id} is not found")
    # return {"post_details":post}
    
    test_post=db.query(models.Post).filter(models.Post.id==id).first()
    print(test_post)
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} is not found")
    return test_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleate_post(id:int, db:Session=Depends(get_db)):
    #deleating the post 
    # index=find_post_index(id)
    # my_post.pop(deleated_post)
    # return {"message":"post was successfully deleted"}
    # we dont send any data back
    
    
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning*""",(str(id),))
    # deleated_post=cursor.fetchone()
    # conn.commit()
    
    post=db.query(models.Post).filter(models.Post.id==id)
    
    
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} is not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemans.Post)
def update_post(id:int,post:schemans.PostCreate, db:Session=Depends(get_db)):
    # print(post)
    # index=find_post_index(id)
    # post_dict=post.dict()
    # post_dict["id"]=id
    # my_post[index]=post_dict
    
    # cursor.execute("""UPDATE posts SET title=%s , contents=%s , published=%s WHERE id=%s""",
    #                (post.title,post.contents,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id == id)
    Post=post_query.first()
    
    if Post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with the id {id} is not found")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()