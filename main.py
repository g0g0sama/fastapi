from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Json
from dataclasses import dataclass


app = FastAPI()

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


my_posts = [{"title": "kırlarda oyun oynamak", "content": "güzldr", "id":1}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/")


def root():

    return {"message": "Hello world! bitches"}


@app.get("/posts")

def get_posts():
    return {"data": "dis is your posts"}


@app.post("/posts")

async def create_posts(new_post:Post):

    print(new_post.title)

    return {"data": "new post"}


@app.get("/posts/{id}")

def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we did not find the post {id}")
    return {"post_detail": post}
