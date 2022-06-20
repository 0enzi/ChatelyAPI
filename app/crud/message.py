from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.chat import Message as MessageSchem, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageSchem, MessageUpdate]):
    # Declare model specific CRUD operation methods.
    pass


message = CRUDMessage(Message)
