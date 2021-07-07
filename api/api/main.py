"""
references:
https://www.toptal.com/python/build-high-performing-apps-with-the-python-fastapi-framework
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
