from typing import List
from uuid import uuid4
from app.models.user import User as UserModel
from app.schemas import user as user_schema
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.api.deps import get_db 
from app import utils
import time

router = APIRouter()

@router.get('/', response_model=List[user_schema.UserOut])
def get_users(db: Session = Depends(get_db)):

     users = db.query(UserModel).all()

     if not users:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} was not found')
     
     return users 

@router.get('/{id}', response_model=user_schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

     user = db.query(UserModel).filter(UserModel.id ==id).first()

     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} was not found')
     
     return user

@router.get('/me', response_model=user_schema.UserOut)
def get_user( db: Session = Depends(get_db), current_user: UserModel = Depends(utils.get_current_user)):

     user = db.query(UserModel).filter(UserModel.id ==current_user.id).first()

     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} was not found')
     
     return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
     timestamp = time.time()
     hashed_pw = utils.get_hashed_password(user.password)
     user.password = hashed_pw
     user.websocket_id = str(timestamp)
     new_user = UserModel(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user 


# @router.post('/signup', summary="Create new user", response_model=user_schema.UserOut)
# async def create_user(data: user_schema.UserAuth, db: Session = Depends(get_db)):
    # querying database to check if user already exist
#     user = db.get(data.email, None)
#     if user is not None:
#             raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exist"
#         )
#     user = {
#         'email': data.email,
#         'password': utils.get_hashed_password(data.password),
#         'id': str(uuid4())
#     }
#     db[data.email] = user    # saving user to database
#     return user

