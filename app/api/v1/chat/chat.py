
from typing import List, Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import time
from app import schemas, crud
from app.models import inbox as inbox_model
from app.schemas import chat as message_schema
from app.api.deps import get_db

router = APIRouter()



# @router.get("", response_model=List[message_schema.Message])
@router.get("")
def read_messages(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all messages.
    """
     
    messages = crud.message.get_multi(db, skip=skip, limit=limit)
    return messages



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
    


@router.post("", response_model=message_schema.MessageCreate)
def create_message(*, db: Session = Depends(get_db), message_in: message_schema.Message, background_tasks: BackgroundTasks) -> Any:
    """
    Create new messages.
    """
    message_in.timestamp = str(time.time())
    # print(message_in)

    # crud.message.create(db, obj_in=message_in)

    ''' 
    INBOX: 
    Check if inbox exists, if not, create
    if it exists update read to false and latest message
    inbox is a connection between the sender and the recipient
    inbox helps us filter
    '''
    background_tasks.add_task(update_inbox, message_in, db)


    return message_in # potential bug
