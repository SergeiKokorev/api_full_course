from fastapi import (FastAPI, Depends, Response, 
                    HTTPException, status, APIRouter)
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils, oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session=Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: Session=Depends(get_db), 
    get_current_user: int = Depends(oauth2.get_current_user)
    ):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found.")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The post with id: {id} doesn't exist")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
        
    return updated_post.first()
