from sqlalchemy import ForeignKey, Column, Integer, String
from database.models.core import Base




class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  
    is_group = Column(Integer, default=0)  



class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)  
    user_id = Column(Integer, nullable=False)  
