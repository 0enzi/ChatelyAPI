from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
from app.database.base_class import Base

# 
class Inbox(Base):
    __tablename__ = "inbox"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    sender_id = Column(Integer)
    unread_count = Column(Integer)
    last_message = Column(String)
    inbox_hash = Column(String)

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    msg = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    read_only = Column(Boolean, nullable=False)
    
