from typing import List, Optional

from pydantic import BaseModel


class FeedItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class FeedItemCreate(FeedItemBase):
    pass


class FeedItem(FeedItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: int
    is_active: bool
    feed_items: List[FeedItem] = []

    class Config:
        orm_mode = True
