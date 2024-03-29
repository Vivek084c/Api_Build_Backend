from fastapi import Response,HTTPException,status,Depends,APIRouter
from .. import schemans,database, models, oauth
from sqlalchemy.orm import Session

router=APIRouter(   
    prefix="/vote",
    tags=["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemans.Vote, db: Session=Depends(database.get_db), current_user:int=Depends(oauth.get_current_user)):
    if not db.query(models.Post).filter(models.Post.id==vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post not found to vote")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on the post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added the vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}

        
