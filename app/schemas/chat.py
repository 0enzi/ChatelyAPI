from pydantic import BaseModel


class Message(BaseModel):
    id: int
    from_id: int
    to_id: int
    msg: str
    datetime: str
    message: str


class Inbox(BaseModel):
    id: int
    user_id: int # owner of the inbox
    sender_id: int # sender of the message
    unread_count: int # number of unread messages
    last_message: str # last message in the inbox