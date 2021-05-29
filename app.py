from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Text
from datetime import datetime

app = FastAPI()

postdb = []


# post model
class Post(BaseModel):
    id: int
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: datetime


@app.get("/")
async def read_root():
    return {"home": "Home page"}


@app.get("/blog")
async def get_posts():
    return postdb


@app.post("/blog")
async def add_post(post: Post):
    postdb.append(post.dict())
    return postdb[-1]


@app.get("/blog/{post_id}")
async def get_post(post_id: int = Path(..., gt=0)):
    post = post_id - 1
    return postdb[post]


@app.put("/blog/{post_id}")
def update_post(post_id: int, post: Post):
    postdb[post_id - 1] = post
    print(post)
    return {"message": "Post has been updated succesfully!"}


@app.delete("/blog/{post_id}")
def delete_post(post_id: int):
    postdb.pop(post_id-1)
    return {"message": "Post has been deleted succesfully"}
