from pydantic import BaseModel


class Message(BaseModel):
    id: int
    from_id: int
    to_id: int
    msg: str
    datetime: str
    message: str
