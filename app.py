from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime

app = FastAPI()


# post model
class Blog(BaseModel):
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: datetime


class updateBlog(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[Text] = None
    updated_at: datetime = datetime.now()
    published_at: datetime


blogdb = {}


@app.get("/")
async def home():
    return {"home": "Home page"}


@app.get("/blog")
async def get_blogs():
    return blogdb


@app.post("/create-blog/{blog_id}")
async def create_blog(blog_id: int, blog: Blog):
    if blog_id in blogdb:
        raise HTTPException(status_code=400, detail="Blog ID already exists.")
    blogdb[blog_id] = blog
    return blogdb[blog_id]


@app.get("/get-blog/{blog_id}")
async def get_blog(blog_id: int = Path(None,
                                       description="ID of your blog entry.",
                                       gt=0)):
    if blog_id not in blogdb:
        raise HTTPException(status_code=404, detail="Blog ID not found.")
    else:
        return blogdb[blog_id]


@app.patch("/update-blog/{blog_id}")
def update_blog(blog_id: int, blog: updateBlog):
    if blog_id not in blogdb:
        raise HTTPException(status_code=404, detail="Blog ID not found.")

    if blog.title is not None:
        blogdb[blog_id].title = blog.title
    if blog.author is not None:
        blogdb[blog_id].author = blog.author
    if blog.content is not None:
        blogdb[blog_id].content = blog.content
    return {"message": "Blog has been updated succesfully!"}


@app.delete("/delete-blog/{blog_id}")
def delete_blog(blog_id: int):
    if blog_id not in blogdb:
        raise HTTPException(status_code=404, detail="Blog ID not found.")
    del blogdb[blog_id]
    return {"message": "Blog has been deleted succesfully"}
