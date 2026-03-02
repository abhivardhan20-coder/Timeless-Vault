from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)


class Nominee(Base):
    __tablename__ = "nominees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nominee_email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AccessRequest(Base):
    __tablename__ = "access_requests"

    id = Column(Integer, primary_key=True, index=True)
    vault_item_id = Column(Integer, ForeignKey("vault_items.id"))
    requester_email = Column(String)
    approval_count = Column(Integer, default=0)
    is_approved = Column(Boolean, default=False)
class VaultItem(Base):
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    encrypted_data = Column(Text)
    file_hash = Column(String, index=True)
    category = Column(String)
    summary = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")