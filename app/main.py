import psycopg
import time


from sqlalchemy.orm import Session
from psycopg.types.json import Jsonb
from fastapi.params import Body
from fastapi import FastAPI


from . import models, schemas
from .database import engine, get_db
from . routers import post, user


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api!!!"}
