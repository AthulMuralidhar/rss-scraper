from sqlalchemy.orm import Session

from .models import User, FeedItems
from .schemas import UserCreate, FeedItemCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    # import ipdb;ipdb.set_trace();

    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user_db(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FeedItems).offset(skip).limit(limit).all()



def create_user_feed(db: Session, feed: FeedItemCreate, user_id: int):
    db_feed = FeedItems(**feed.dict(), user_id=user_id)
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    return db_feed
