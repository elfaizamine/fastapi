
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from typing import List
from sqlalchemy.orm import Session
from ..database import engine, get_db





router = APIRouter()






@router.get("/posts", response_model = List[schemas.PostResponse])

def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" select * from posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts




@router.get("/posts/{id}", response_model = schemas.PostResponse)

def get_post_id(id : int, db: Session = Depends(get_db)):

    #cursor.execute(""" select * from posts where id = %s """, (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post with id: {id} not found"}

    return post





@router.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)

def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

    #cursor.execute(""" insert into posts (title, content, published) \
    #               VALUES (%s, %s, %s) returning * """, \
    #               (post.title, post.content, post.published))
    
    #post_dict = cursor.fetchone()
    #conn.commit()




@router.delete("/posts/{id}")
def delete_posts(id:int, status_code = status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db)):

    #cursor.execute(""" delete from posts where id = %s returning * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = "id doesn't exists")

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)




@router.put('/posts/{id}', response_model = schemas.PostResponse)
def update_id(id : int, post11 : schemas.PostUpdate, db: Session = Depends(get_db)):

    #cursor.execute(""" update  posts set title = %s , content = %s, published = %s \
    #               where id = %s returning * """, (post.title, post.content, \
    #                                               post.published, str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = "id doesn't exists")
    
    post_query.update(post11.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
