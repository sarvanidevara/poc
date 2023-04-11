from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ... import hashservice
from ...models import base
from . import schemas
from app.db.database import get_db


# Set prefix to routes
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

 # Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):    
    #hash pwd    
    user.password = hashservice.hash(user.password)    
    new_user = base.user.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user

#Api to get user details wrt path parameter 'id'
@router.get("/{id}", response_model=schemas.UserOut) 
def getUser(id: int, db: Session = Depends(get_db)):
    userDet = db.query(base.user.User).filter(base.user.User.id == id).first()
    if not userDet:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User Record with id:{id} not found")        
    return userDet    

