from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session;


from .database import SessionLocal, engine
from .schemas import UserCreate, User, Feed, FeedCreate
from .crud import get_user_by_email, create_user, get_users, get_user, create_user_feed, get_feeds
from .models import Base

from bs4 import BeautifulSoup
import requests

import logging


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/feeds/", response_model=Feed)
def create_item_for_user(
    user_id: int, feed: FeedCreate, db: Session = Depends(get_db)
):
    return create_user_feed(db=db, feed=feed, user_id=user_id)


@app.get("/feeds/", response_model=List[Feed])
def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feeds = get_feeds(db, skip=skip, limit=limit)
    return feeds



# background task routes
async def get_feed_items(feed_url: str):
    page = await requests.get(feed_url)

    logging.info("REQUEST COMPLETED")

    soup = BeautifulSoup(page.content, 'lxml')

    for item in soup.find_all('item'):
        yield item


@app.post("/background-tasks/populate-feeds/{url}")
async def get_feeds(feed_url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(get_feed_items, feed_url)
    return {"message": "Notification sent in the background"}