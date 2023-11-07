from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, get_db



models.Base.metadata.create_all(bind=engine)


app = FastAPI()



@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    print(1)

    try:
        post = db.query(models.Post).all()
        print('yes', post)
    except Exception as e:
        print('no', e)


    return {"data" : post}





class Post(BaseModel):
    title:str
    content:str
    published: bool = True



##### START ###############################################
"""
while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi',\
                                user = 'aelfaiz', password = 'pass123',\
                                    cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Sucessful')
        break
    except Exception as error:
        time.sleep(2)
        print(error)
        print('Failed')
"""




#############################  GET ALL DATA OR ONE ID ##########################

@app.get("/posts")

def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" select * from posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)

def create_posts(post : Post, db: Session = Depends(get_db)):

    
    new_post = models.Post(title = post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data" : new_post}

    #cursor.execute(""" insert into posts (title, content, published) \
    #               VALUES (%s, %s, %s) returning * """, \
    #               (post.title, post.content, post.published))
    
    #post_dict = cursor.fetchone()
    #conn.commit()













