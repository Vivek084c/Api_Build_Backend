from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemans,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema=OAuth2PasswordBearer(tokenUrl='login')


#SECRET_KEY
#Algorithm
#Expriation time


SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUITES=settings.access_token_expire_minutes

def create_access_token(data:dict):
    encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUITES)
    encode.update({"exp":expire})
    
    encoded_jwt=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

#fuction to verify access token
def verify_access_token(token:str,credentials_exceptions):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if not id:
            raise credentials_exceptions
        token_data=schemans.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions
    return token_data

def get_current_user(token:str=Depends(oauth2_schema), db:Session=Depends(database.get_db) ):
    credentials_exceptions=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate the credentails ",headers={"WWW-  Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exceptions)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user 
    
    
    