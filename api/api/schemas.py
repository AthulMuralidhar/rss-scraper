from typing import List, Optional

from pydantic import BaseModel


class FeedBase(BaseModel):
    title: str
    description: Optional[str] = None


class FeedCreate(FeedBase):
    pass


class Feed(FeedBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: int
    is_active: bool
    feeds: List[Feed] = []

    class Config:
        orm_mode = True
