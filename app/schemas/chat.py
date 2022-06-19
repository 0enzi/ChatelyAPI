from pydantic import BaseModel


class Message(BaseModel):
    id: int
    from_id: int
    to_id: int
    msg: str
    datetime: str
    message: str


############################################
#### (🧑🏼‍🦲) John Doe              ############
##### Latest message here 10:12 ############
class Inbox(BaseModel):
    id: int 
    user_id: int # owner of the inbox
    sender_id: int # sender of the message
    unread_count: int # number of unread messages
    last_message: str # last message in the inbox
    
    #unique hash that helps us query to a certain inbox
    inbox_hash: str # <latest_msg_id>:<sender_id>: 