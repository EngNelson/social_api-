from types import new_class
from enum import auto
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import model, schema, utils
from .database import engine, get_db
from .routers import post, user, auth



# model.Base.metadate.create_all(bind=engine)


app = FastAPI()


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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api and i love python"}
   


# @app.get("/posts", response_model=List[schema.Post])
# def get_posts(db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts """)
#     # posts = cursor.fetchall()
#     # # print(posts)

#     posts = db.query(model.Post).all()
#     return posts


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
# def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
   
 

#     new_post = model.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)


#     return new_post




# @app.get("/posts/{id}", response_model=schema.Post)
# def get_post(id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
#     # post  = cursor.fetchone()
#     post = db.query(model.Post).filter(model.Post.id == id).first()
   
    

    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"post with id: {id}was not found")
#     return  post 


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):

#     # cursor.execute("""DELETE FROM posts   WHERE id = %s returning *""", (str(id),))
#     # delete_post = cursor.fetchone()
#     # conn.commit()

#    post = db.query(model.post).filter(model.Post.id == id)
   

#    if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exist")

#    post.delete(synhronize_session=False)
#    db.commit()
   
#    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", response_model=schema.Post)
# def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):

#     # print(id)
#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
#     # """, 
#     # (post.title,post.content, post.published, str(id)))

#     # updated_post = cursor.fetchone()
#     # conn.commit() 
  
#     post_query = db.query(model.Post).filter(model.Post.id == id)

#     post = post_query.first()

#     # if post == None:
    
    


#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exist")

#     post_query.update(updated_post.dict(), synchronize_session=False)

#     db.commit()

    

#     return post_query.first()


# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
# def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

#        #hash the password -user.password
    
#     hashed_password =  utils.hash(user.password)
#     user.password = hashed_password


#     new_user = model.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user
 
# @app.get('/users/{id}', response_model=schema.Userout)
# def get_user(id: int, db: Session = Depends(get_db)):
#  user = db.query(model.User).filter(model.User.id == id).first()
#  if not user:
#      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

#  return user

