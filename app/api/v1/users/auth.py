from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils import get_refresh_user
from app import utils
from app.api.deps import get_db
from app.models.user import User as UserModel

router = APIRouter()
session = Session()

# @router.post('/login')
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

#     user = db.query(UserModel).filter(UserModel.email == user_credentials.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

#     access_token = oauth2.create_access_token(data= {"user_id": user.id}) 
#     return {'access_token': access_token, 'token_type': 'bearer'}
    

@router.post('/login', summary="Create access and refresh tokens for user") #, response_model=TokenSchema
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Query for user
    q_user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    # print(user.__dict__['password'])
    if q_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    user = q_user.__dict__ # we want the iterable dictionary not an object

    

    hashed_pass = user['password']
    if not utils.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    

    encoded_user = {
        'username': user['email'],
        'user_id': user['id'],
    }
    return {
        "access_token": utils.create_access_token(encoded_user),
        "refresh_token": utils.create_refresh_token(user['email']),
    }


@router.post('/refresh', summary="Create access token for user with refresh token") #, response_model=TokenSchema
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
        
    user = get_refresh_user(db, refresh_token).__dict__
    encoded_user = {
        'username': user['email'],
        'user_id': user['id'],
    }

    return {
        "access_token": utils.create_access_token(encoded_user)
    }

