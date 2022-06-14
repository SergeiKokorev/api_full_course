import psycopg
import time


from sqlalchemy.orm import Session
from psycopg.types.json import Jsonb
from fastapi import FastAPI, Depends, Response, HTTPException, status
from fastapi.params import Body
from typing import Optional, List
from random import randrange

from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:

    try:
        conn = psycopg.connect(
            host="localhost",
            dbname="fastapi",
            password="ks1200ks",
            user="sergei",
        )
        cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
        print("Database connection was succesful!")
        break
    except Exception as error:
        print(f"Connecting to database failed with error: {error}")
        time.sleep(3)


def db_connect(db_host, db_name, db_user, db_passwd):
    try:
        conn = psycopg.connect(
            host=db_host, 
            database=db_name, 
            user=db_user, 
            password=db_passwd)
        print("Database connection was succesfull!")
        return conn
    except psycopg.Error as er:
        print("Database connection was failed with erro: {er}")
        return f"Database connection was failed with error {er}."


def find_post(id):
    return [post for post in my_posts if post['id'] == id]


def find_index_post(id):
    try:
        index = next(i for i, post in enumerate(my_posts) if post['id'] == id)
    except StopIteration:
        index = None
    return index


@app.get("/")
def root():
    return {"message": "Welcome to my appi!!!"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session=Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found")

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found.")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The post with id: {id} doesn't exist")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
        
    return updated_post.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBack)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


if __name__ == "__main__":
    
    host = "localhost"
    db = "fastapi"
    user = "sergei"
    password = "ks1200ks"
    # conn = db_connect(host, db, user, password)
    # print(conn)
    # curs = conn.cursor()
    # get_posts(curs)
