from fastapi import APIRouter,Depends,status, HTTPException, responses
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database,schemans,models,utils,oauth

router=APIRouter(tags=["authentication"])

@router.post("/login",response_model=schemans.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    #retriving the user data from database
      #oauth2request will return two files: 1)username and 2)password
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials")
    #hashing the passwrod from frontend and comparing with the databse to check if password is correct
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credentials")
    
    #creating a tokken 
    access_token=oauth.create_access_token(data={"user_id":user.id})
    #return toekn
    return {"access_token":access_token, "token_type":"bearer"}