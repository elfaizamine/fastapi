


@app.get("/posts/{id}")

def get_post_id(id : int, response : Response):

    cursor.execute(""" select * from posts where id = %s """, (str(id)))

    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post with id: {id} not found"}

    return {"data_id" : post}

"add a feature"

"third commit"

"create new branch"







#############################  POST DATA CREATE ID ##########################





@app.post("/posts", status_code = status.HTTP_201_CREATED)

def create_posts(post : models.Post):

    cursor.execute(""" insert into posts (title, content, published) \
                   VALUES (%s, %s, %s) returning * """, \
                   (post.title, post.content, post.published))
    
    post_dict = cursor.fetchone()
    conn.commit()
    return {"data" : post_dict}











#############################  DELETE POST ##########################

@app.delete("/posts/{id}")
def delete_posts(id:int, status_code = status.HTTP_204_NO_CONTENT):

    cursor.execute(""" delete from posts where id = %s returning * """, (str(id)))

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = "id doesn't exists")
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)



#############################  UPDATE POST ##########################


@app.put('/posts/{id}')
def update_id(id : int, post : Post):

    cursor.execute(""" update  posts set title = %s , content = %s, published = %s \
                   where id = %s returning * """, (post.title, post.content, \
                                                   post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()



    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = "id doesn't exists")

    return {"data": updated_post}