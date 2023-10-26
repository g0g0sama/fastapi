from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, Json
from dataclasses import dataclass
import psycopg
from psycopg.rows import dict_row
import time

from . import models, schemas, utils

from .database import engine, get_db

from sqlalchemy.orm import Session
from typing import Optional, List

from .routers import post, user




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

app.include_router(post.router)

app.include_router(user.router)


@app.get("/")
def root():

    return {"message": "Hello world! bitches"}

