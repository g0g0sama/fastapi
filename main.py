from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Json
from dataclasses import dataclass


app = FastAPI()



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


@app.post("/createposts")

async def create_posts(new_post:Post):

    print(new_post.title)

    return {"data": "new post"}