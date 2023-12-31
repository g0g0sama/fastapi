from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from typing import   List
from ..database import  get_db


router = APIRouter(prefix="/posts",
                   tags= ["Posts"])


@router.get("/", response_model= List [schemas.Post])

def get_posts(db: Session = Depends(get_db)):


    
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)

def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user.email)
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/{id}", response_model= schemas.Post)

def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    print(current_user.email)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we did not find the post {id}")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    


    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no {id}")

    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")

def update_post(id:int, updated_post:schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
 

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no {id}")
    
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()

    return post_query.first()