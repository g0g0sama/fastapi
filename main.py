from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Json
from dataclasses import dataclass
import psycopg
from psycopg.rows import dict_row
import time




app = FastAPI()


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

my_posts = [{"title": "kırlarda oyun oynamak", "content": "güzldr", "id":1}]

class Post(BaseModel):
    name: str
    price: int



while True:
    try:
        conn = psycopg.connect(host = "/var/run/postgresql", dbname   = "fastapi", \
            user = "goksucan", password = "123456jl789g", row_factory=dict_row)
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

def get_posts():
    
    cursor.execute("""SELECT * FROM products    """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)

async def create_posts(post:Post):
    cursor.execute("""INSERT INTO products (name, price) VALUES (%s, %s) RETURNING * """,
                   (post.name, post.price))

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}")

def get_post(id: int):
    cursor.execute("""SELECT * FROM products WHERE id = %s """, (str(id),))
    
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"we did not find the post {id}")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int):
    cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id),))
    
    deleted_post = cursor.fetchone()

    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no {id}")


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")

def update_post(id:int, post:Post):
    cursor.execute("""UPDATE products SET name = %s, price = %s WHERE id=%s RETURNING * """, 
                   (post.name, post.price, str(id)))

    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"no {id}")

    return {"data": updated_post}