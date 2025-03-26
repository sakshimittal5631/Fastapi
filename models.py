from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True)
    password = Column(String(200))

    created_rooms = relationship("ChatRoom", back_populates="creator")
    sent_messages = relationship("Message", back_populates="sender")



class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(500))
    created_by = Column(Integer, ForeignKey("users.id"))
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)  # new field
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    creator = relationship("User", back_populates="created_rooms")
    workspace = relationship("Workspace", back_populates="channels")  # new relationship
    members = relationship("RoomMember", back_populates="room")
    messages = relationship("Message", back_populates="room")



class RoomMember(Base):
    __tablename__ = 'room_members'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), index=True)
    room_id = Column(Integer, ForeignKey('chat_rooms.id'))

    room = relationship("ChatRoom", back_populates="members")

    __table_args__ = (UniqueConstraint("user_name", "room_id", name="_user_room_uc"),)



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    sender_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    sender = relationship("User", back_populates="sent_messages")
    room = relationship("ChatRoom", back_populates="messages")


class RoomInviteToken(Base):
    __tablename__ = "room_invite_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(500))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())

    channels = relationship("ChatRoom", back_populates="workspace")
