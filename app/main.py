# from types import new_class
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import model
# from . import Base
from .database import engine, get_db

model.Base.metadate.create_all(bind=engine)


app = FastAPI()







class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    name: str
    id: str
    created_at: str

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='psnelson', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!!")
        break 

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)   


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":
"favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 


@app.get("/")
def root():
    return {"message": "Welcome to my api and i love python"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(model.Post).all()
    return{"data": posts}    


@app.get("/posts")
def get_posts():
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # # print(posts)
    return{"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
   
    # cursor.execute(""" INSERT INTO posts (title, content, published, name, id, created_at) 
    # VALUES (%s, %s, %s, %s, %s, %s) RETURNING
    # * """,
    #         (post.title,post.content, post.published, post.name, post.id, post.created_at))
    # new_post = cursor.fetchone()

    # conn.commit()
    # print(**post.dict())
    new_post = model.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return{"data": new_post}




@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post  = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
   
    

    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id}was not found")
    return {"post_detail":  post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts   WHERE id = %s returning *""", (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()

   post = db.query(model.post).filter(model.Post.id == id)
   

   if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

   post.delete(synhronize_session=False)
   db.commit()
   
   return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post:Post, db: Session = Depends(get_db)):

    # print(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
    # """, 
    # (post.title,post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit() 
  
    post_query = db.query(model.Post).filter(model.Post.id == id)

    post = post_query.first()

    # if post == None:
    
    


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    

    return{"data": post_query.first()}


