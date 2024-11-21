from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database.models.core import Base




class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)    
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False) 
    text = Column(String, nullable=False)        
    timestamp = Column(DateTime, server_default=func.now())
