# from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
# from app.database.base_class import Base

# class Message(Base):
#     __tablename__ = "message"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     sender_id = Column(Integer, nullable=False)
#     recipient_id = Column(Integer, nullable=False)
#     msg = Column(String, nullable=False)
#     timestamp = Column(String, nullable=False)
#     read = Column(Boolean, default=False)