from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.sql import func

from .database import Base


"""
design decisions:

1. follow and un-follow multiple fields
- folowing is defined by setting a user id on a feed item
- unfollowing is defined by un setting the user id


"""

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    feed_items = relationship("FeedItems", back_populates="user")


class FeedItemStatusEnum(enum.Enum):
    read = 'read'
    unread = 'unread'

class FeedItems(Base):

    __tablename__ = "feeditems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    feed_item_status = Column(Enum(FeedItemStatusEnum),default=FeedItemStatusEnum.unread, index=True)
    time_updated =  Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="feed_items")
