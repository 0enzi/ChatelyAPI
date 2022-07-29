from typing import List, Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils import get_current_user
from app.models import inbox as inbox_model
from app.models.user import User
from app.api.deps import get_db
from app.schemas.chat import MessageCreate
import redis
from redis import Redis
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


@router.get('/mine')
def get_my_inbox(current_user: str = Depends(get_current_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all inboxes.
    """
    inbox_list = db.query(inbox_model.Inbox).all()
    my_inbox_list = []
    for inbox in inbox_list:
        inbox_hash = inbox.__dict__['inbox_hash'].split('-')
        if f'{current_user.id}' in inbox_hash:
            my_inbox_list.append(inbox)
    

    '''
    Retouch the to auto detect who's the sender
    '''
    retouched_inbox = []
    for inbox in my_inbox_list:
        inbox_ids = inbox.__dict__['inbox_hash'].split('-')
        if str(current_user.id) in inbox_ids:
            inbox_ids.remove(str(current_user.id))
        else:
            print("error")
        # retouch 
        inbox.__dict__['sender_id'] = int(inbox_ids[0])
        inbox.__dict__['reciepient_id'] = int(current_user.id)
        inbox.__dict__['profile'] = current_user.profile
        reciepient_item = db.query(User).filter(User.id == int(inbox_ids[0])).first()
        if reciepient_item:
            inbox.__dict__['sender_name'] = db.query(User).filter(User.id == int(inbox_ids[0])).first().__dict__['username']
        else: 
            inbox.__dict__['sender_name'] = "John Doe"
        
        retouched_inbox.append(inbox.__dict__)
 


    

    if not my_inbox_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No inboxes yet')
     
    return my_inbox_list

@router.get("/{inbox_hash}")
def get_one_inbox(inbox_hash, current_user : str = Depends(get_current_user),  db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all inboxes.
    """
    ids = inbox_hash.split('-')
    if str(current_user.id) not in ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'You ({current_user.id}) are not authorized to access this inbox')
    
    
    inbox_item = db.query(inbox_model.Inbox).filter_by(inbox_hash = inbox_hash).first()
    if inbox_item:
        return {inbox_item}
    raise HTTPException(status_code=404, detail="Inbox not found did you mean its reverse")


# Should be updated everytime a message is sent
@router.post("/update")
async def update_inbox(new_message: MessageCreate, db: Session = Depends(get_db)):

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


def connect_to_redis():
    hostname = "localhost"
    port = 6379

    r = Redis(hostname, port, retry_on_timeout=True)
    return r


def get_data(redis_connection, inbox_hash:str):
    '''
    Get data from redis w/xread
    '''
    last_id = 0
    # sleep_ms = 5000
    stream_key = f'0_0_0_0:{inbox_hash}:stream'
    messages_list = []
    

    for i in range(15):
        try:
            resp = redis_connection.xread(
                {stream_key: last_id}, count=1
            )
            if resp:
                key, messages = resp[0]
                last_id, data = messages[0]
                
                # print("REDIS ID: ", last_id)
                msg_dict = {
                    'username': data[b'uname'].decode('utf-8'),
                    'msg': data[b'msg'].decode('utf-8'),
                }
                # print(i, msg_dict)
                # print(msg_dict)
                messages_list.append(msg_dict)
    
        except ConnectionError as e:
            print("ERROR REDIS CONNECTION: {}".format(e))
        
    return messages_list


@router.get("/msg/{inbox_hash}")
async def get_chats_in_inbox(inbox_hash: str, current_user : str = Depends(get_current_user),  db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve latest messages from inbox
    """
    
    connection = connect_to_redis()
    messages = get_data(connection, inbox_hash)
    
    return messages
