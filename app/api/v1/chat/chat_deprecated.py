'''     _                               _           _
  __| | ___ _ __  _ __ ___  ___ __ _| |_ ___  __| |
 / _` |/ _ \ '_ \| '__/ _ \/ __/ _` | __/ _ \/ _` |
| (_| |  __/ |_) | | |  __/ (_| (_| | ||  __/ (_| |
 \__,_|\___| .__/|_|  \___|\___\__,_|\__\___|\__,_|
           |_|

 Feel free to delete :D

'''
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
