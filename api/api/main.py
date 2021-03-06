from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.logger import logging
from sqlalchemy.orm import Session


from .database import SessionLocal, engine
from .schemas import UserCreate, User, FeedItem, FeedItemCreate
from .crud import (
    get_user_by_email,
    create_user_db,
    get_users,
    get_user,
    create_user_feed,
    get_feeds,
)
from .models import Base

from bs4 import BeautifulSoup
import requests

import json


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

    # import ipdb;ipdb.set_trace();

    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user_db(db=db, user=user)


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


@app.post("/users/{user_id}/feeds/", response_model=FeedItem)
def create_item_for_user(
    user_id: int, feed: FeedItemCreate, db: Session = Depends(get_db)
):
    return create_user_feed(db=db, feed=feed, user_id=user_id)


@app.get("/feeds/", response_model=List[FeedItem])
def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feeds = get_feeds(db, skip=skip, limit=limit)
    return feeds


@app.post("/background-tasks/populate-feeds/{url}")
async def populate_feeds(feed_url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(get_feed_items, feed_url)
    return {"message": "feed items creation added to background tasks"}


# background task routes
async def get_feed_items(feed_url: str):
    try:
        page = requests.get(feed_url)
        soup = BeautifulSoup(page.content, "lxml")
        response = None

        for item in soup.find_all("item"):
            feed = {
                "title": item.title.text,
                "description": item.description.text,
            }
            response = create_user_feed(db=SessionLocal(), feed=feed, user_id=1)

            print({"added": response})

    except Exception:
        return {"result": "failed"}
    finally:
        return {"result": "successful"}
