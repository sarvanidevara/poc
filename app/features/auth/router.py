from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.db import database
from ... import oauth2
from ... import hashservice
from ...models import base
from . import schemas

router = APIRouter(tags=['Authentication'])

# Note : user_credentials.username == OAuth2PasswordRequestForm stores email in 'username', and password in 'password'
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(base.user.User).filter(base.user.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not hashservice.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials pwd')

    #Create token    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    # return token
    return {"access_token": access_token, "token_type": "bearer"}