import email
from app.database.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text( 'now()'))
    is_active = Column(Boolean, default=True)
    user_type = Column(Integer, default=0)
    websocket_id = Column(String, unique=True, index=True)
    profile = Column(String, default='default_img.png')
    
    # items = relationship("Item", back_populates="owner")
    
