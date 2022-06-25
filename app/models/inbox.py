from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
from app.database.base_class import Base


class Inbox(Base):
    __tablename__ = "inbox"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    sender_id = Column(Integer)
    unread_count = Column(Integer)
    last_message = Column(String)
    inbox_hash = Column(String) # 23-32 sender id 