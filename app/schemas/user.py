from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    active: Optional[bool] = True
    status: bool
    profile: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    profile: str

    class Config:
        orm_mode = True
