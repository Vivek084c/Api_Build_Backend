from .. import models,schemans,utils
from fastapi import Response,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db

router=APIRouter(
    prefix="/users",tags=["users"]
)

#routs for user path operations
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemans.UserOut)
def create_user(user:schemans.UserCreate, db:Session=Depends(get_db)):
    #hasing the password
    hashed_password=utils.hash(user.password)
    user.password = hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}',response_model=schemans.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user with the id {id} is not found")
    return user
    