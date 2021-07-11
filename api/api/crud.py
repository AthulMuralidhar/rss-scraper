from sqlalchemy.orm import Session

from models import User, Feed
from schemas import UserCreate, FeedCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()



def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Feed).offset(skip).limit(limit).all()



def create_user_feed(db: Session, feed: FeedCreate, user_id: int):
    db_feed = Feed(**feed.dict(), owner_id=user_id)
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    return db_feed
