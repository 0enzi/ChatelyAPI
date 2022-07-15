from typing import List, Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import time
from app.utils import get_current_user
from app import schemas, crud
from app.models import inbox as inbox_model
from app.api.deps import get_db

router = APIRouter()


@router.get("/all")
def get_inbox(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all inboxes.
    """
    inbox_list = db.query(inbox_model.Inbox).all()

    if not inbox_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} was not found')
     
    return inbox_list


@router.get("/{inbox_hash}")
def get_one_inbox(inbox_hash, current_user : str = Depends(get_current_user),  db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all inboxes.
    """
    ids = inbox_hash.split('-')
    if current_user.id not in ids:
        return {'message': 'You are not authorized to view this inbox'}
    inbox_item = db.query(inbox_model.Inbox).filter_by(inbox_hash =  inbox_hash).first()
    # inbox_list = db.query(inbox_model.Inbox).all()


   
    return {inbox_item}



# Should be updated everytime a message is sent
def update_inbox(new_message, db: Session):

    # Get sender and recipient ids and create an inbox hash
    inbox_hash = f'{new_message.sender_id}-{new_message.recipient_id}'
    exists = db.query(inbox_model.Inbox).filter(inbox_model.Inbox.inbox_hash == inbox_hash).first() is not None
    
    if exists: # dont think if else is needed asthey both do the same thing
        inbox_item = db.query(inbox_model.Inbox).filter_by(inbox_hash =  inbox_hash).one()
        inbox_item.last_message = new_message.msg

        db.add(inbox_item)
        db.commit()
        db.refresh(inbox_item)
    else:
        inbox_item = inbox_model.Inbox(
            inbox_hash=inbox_hash, 
            last_message=new_message.msg,
            user_id=new_message.recipient_id,
            sender_id=new_message.sender_id)
        db.add(inbox_item)
        db.commit()
        db.refresh(inbox_item)
