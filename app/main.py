from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, Json
from dataclasses import dataclass
import psycopg
from psycopg.rows import dict_row
import time

from . import models, schemas

from .database import engine, get_db

from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)





app = FastAPI()




    


while True:
    try:
        conn = psycopg.connect(host = "127.0.0.1", dbname   = "fastapi", \
            user = "postgres", password = "123456789g", row_factory=dict_row)
        cursor = conn.cursor()
        print("db successfully connected.")
        break

    except Exception as error:
        print("me failed.")
        print(f"Error: {error}")
        time.sleep(2)


@app.get("/")
def root():

    return {"message": "Hello world! bitches"}


@app.get("/posts")

def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)

def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    return  new_post


@app.get("/posts/{id}")

def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we did not find the post {id}")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    


    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no {id}")

    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")

def update_post(id:int, updated_post:schemas.PostUpdate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
 

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no {id}")
    
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()

    return post_query.first()