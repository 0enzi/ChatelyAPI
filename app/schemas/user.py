from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    status: bool
    is_active: Optional[bool] = True
    profile: str
    websocket_id: str

class UserUpdate(BaseModel):
    username: str
    # email: EmailStr
    # password: str
    # status: bool
    # is_active: Optional[bool] = True
    profile: str
    # websocket_id: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    active: Optional[bool] = True
    status: bool
    profile: str
    websocket_id: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    id: int
    email: str
    password: str
