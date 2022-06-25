
from typing import List, Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import time
from app import schemas, crud


from app.schemas import chat as message_schema
from app.api.deps import get_db

router = APIRouter()


def update_inbox(db: Session):
    print(db)

# @router.get("", response_model=List[message_schema.Message])
@router.get("")
def read_messages(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all messages.
    """
     
    messages = crud.message.get_multi(db, skip=skip, limit=limit)
    return messages


# @router.get('/inbox')


@router.post("", response_model=message_schema.Message)
def create_message(*, db: Session = Depends(get_db), message_in: message_schema.Message, background_tasks: BackgroundTasks) -> Any:
    """
    Create new messages.
    """
    message_in.timestamp = str(time.time())
    # print(message_in)

    message = crud.message.create(db, obj_in=message_in)

    ''' 
    INBOX: 
    Check if inbox exists, if not, create
    if it exists update read to false and latest message
    inbox is a connection between the sender and the recipient
    inbox helps us filter
    '''
    background_tasks.add_task(update_inbox)


    print(type(message))
    return message_in # potential bug
