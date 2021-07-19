from api import __version__
import pytest


import pytest
from fastapi import BackgroundTasks
from requests import Response

from api.main import app, get_feed_items
from unittest.mock import mock_open

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base
from api.main import app, get_db
import json
from api.cron import start_background_tasks


"""
https://stackoverflow.com/questions/58270958/mocking-background-tasks-add-task
https://fastapi.tiangolo.com/advanced/async-tests/
https://fastapi.tiangolo.com/advanced/testing-database/
"""


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user():

    # POST
    response = client.post(
        "/users/",
        json={"email": "tester@rss.com", "password": "summertime"},
    )
    try:
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "tester@rss.com"
        assert "id" in data
        user_id = data["id"]


        # GET
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "tester@rss.com"
        assert data["id"] == user_id


    except AssertionError:

        # import ipdb;ipdb.set_trace()

        assert response.status_code == 400
        assert response.json().get('detail') == "Email already registered"

from httpx import AsyncClient

@pytest.mark.asyncio
async def test__get_feed_items():
    URL = "http://www.nu.nl/rss/Algemeen"
    
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        response = await ac.post(f"/background-tasks/populate-feeds/{URL}")
    
    assert response.status_code == 200
    assert response.json() == {"message": "feed items created"}

# @pytest.mark.asyncio
# async def test__start_background_tasks():

def test__start_background_tasks():

    # import ipdb;ipdb.set_trace()
    
    result = start_background_tasks()

    assert result