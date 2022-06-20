from typing import List
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

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
     timestamp = time.time()
     hashed_pw = utils.hash(user.password)
     user.password = hashed_pw
     user.websocket_id = timestamp
     new_user = UserModel(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user 


