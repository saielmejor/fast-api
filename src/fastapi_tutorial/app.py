from fastapi import FastAPI ,HTTPException, status, Depends, Response ,File, UploadFile,Form, Depends 
from src.fastapi_tutorial.schemas import PostCreate , PostResponse
from src.fastapi_tutorial.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession 

from contextlib import asynccontextmanager 
from sqlalchemy import select 
from src.fastapi_tutorial.images import imageKit 
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions 
import shutil 
import os 
import uuid 
import tempfile 

@asynccontextmanager 
async def lifespan(app:FastAPI): 
    await create_db_and_tables() 
    yield 

app=FastAPI(lifespan=lifespan) 

# text_posts={
#     # empty dictionary 
#     1: {
#         "title": "My first post",
#         "content": "This is my first post content"
#     }, 
#     2: {
#         "title": "My second post",
#         "content": "This is my second post content"
#     } ,
#     3: {
#         "title": "My third  post",
#         "content": "This is my third post content"    , 
# },
# 4: {
#         "title": "My fourth  post",
#         "content": "This is my third post content"      
# }
# }
    
 
# @app.get("/posts") 
# def get_all_posts(limit:int=None): 
#     if limit:
#         return list(text_posts.values())[:limit] # convert values into a list 
#     # limit parameters is used tp limit show certain limit 
#     return text_posts 


# @app.get("/posts/{post_id}")
# def get_post(post_id: int):
#     post = text_posts.get(post_id)
#     if post_id not in post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#     return post.get(post_id)

# # Request body 

# @app.post("/posts")

# def create_post(post:PostCreate) -> PostResponse:  # add a validation when you sending the output 
#     new_post={"title": post.title, "content":post.content}
#     text_posts[max(text_posts.keys())+1]=new_post 
#     return new_post 

@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...), 
    caption:str=Form(""), 
    session: AsyncSession=Depends(get_async_session) # dependency injection 


): 
    post = Post( 
        caption= caption, 
        url="dummy url", 
        file_type="photo", 
        file_name="dummy name"
    )

    session.add(post) 
    await session.commit() ## commit to the session to save it to the database
    await session.refresh(post) 
    return post 

@app.get("/feed")
async def get_feed(session:AsyncSession=Depends(get_async_session)

): 
    result=await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts=[ row[0] for row in result.all()] #returns a cursor object and pulling it into individual values 

    posts_data=[] 
    for post in posts: 
        posts_data.append(
            {
                "id":str(post.id), 
                "caption":post.caption, 
                "url": post.url, 
                "filetype":post.file_type, 
                "filename":post.file_name, 
                "created_at":post.created_at.isoformat()
            }
        )

    return {"posts":posts_data}   
