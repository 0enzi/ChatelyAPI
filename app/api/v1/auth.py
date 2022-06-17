from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import utils, oauth2
from app.api.deps import get_db
from app.models.user import User as UserModel

router = APIRouter()

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(UserModel).filter(UserModel.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

    access_token = oauth2.create_access_token(data= {"user_id": user.id}) 
    return {'access_token': access_token, 'token_type': 'bearer'}
    
