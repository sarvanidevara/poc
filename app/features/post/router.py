from fastapi import Response, status, HTTPException, Depends, APIRouter
# Receive data from body in POST(Create post)
from sqlalchemy.orm import Session
from sqlalchemy import func
from ...models import base
from . import schemas
from ... import oauth2
from app.db.database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Read api 
@router.get("/", response_model=List[schemas.PostOut])
def getAllPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
 limit: int = 10, skip: int = 0, search: Optional[str] =""):
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(base.post.Post, func.count(base.post.Vote.post_id).label("votes")).join(base.post.Vote, base.post.Vote.post_id == base.post.Post.id, isouter=True).group_by(base.post.Post.id).filter(base.post.Post.owner_id == current_user.id, base.post.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# Create api
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    new_post = base.post.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post  

#Api to get record details wrt path parameter 'id'
@router.get("/{id}", response_model=schemas.PostOut) 
def getPost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #postDet = db.query(models.Post).filter(models.Post.id == id).first()
    postDet = db.query(base.post.Post, func.count(base.post.Vote.post_id).label("votes")).join(base.post.Vote, base.post.Vote.post_id == base.post.Post.id, isouter=True).group_by(base.post.Post.id).filter(base.post.Post.id == id).first()
    if not postDet:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Record with id:{id} not found")        
    return postDet

@router.put("/{id}", response_model=schemas.Post)
def updatePost(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    post_query = db.query(base.post.Post).filter(base.post.Post.id == id)
    post_exist = post_query.first()

    if post_exist == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Record with id:{id} not found")

    if post_exist.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f'Not authorized')

    post_query.update(post.dict(), synchronize_session=False) 
    db.commit()
    return post_query.first()

# Delete Post
@router.delete("/delete/{id}",status_code=204)
def deletePost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(base.post.Post).filter(base.post.Post.id == id)
    postDet = post.first()
    if postDet == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Record with id:{id} not found")

    if postDet.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f'Not authorized')

    post.delete(synchronize_session=False)
    db.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)