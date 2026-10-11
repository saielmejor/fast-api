from fastapi import FastAPI ,HTTPException, status, Depends, Response ,File, UploadFile,Form, Depends 
from src.fastapi_tutorial.schemas import PostCreate , PostResponse
from src.fastapi_tutorial.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession 
from contextlib import asynccontextmanager 
from sqlalchemy import select 
from src.fastapi_tutorial.images import imagekit 
import shutil 
import os 
import uuid 
import tempfile 

from src.fastapi_tutorial.images import imagekit



@asynccontextmanager 
async def lifespan(app:FastAPI): 
    await create_db_and_tables() 
    yield 

app=FastAPI(lifespan=lifespan) 

@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...), 
    caption:str=Form(""), 
    session: AsyncSession=Depends(get_async_session) # dependency injection 
): 
    temp_file_path= None 
    
    try: 
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as temp_file: 
            temp_file_path=temp_file.name 
            shutil.copyfileobj(file.file, temp_file)
            
        upload_result= imagekit.files.upload(
            file=open(temp_file_path,"rb"), 
            file_name=file.filename, 
            tags=["backend"]
        ) 
        
         
  
            
        post = Post( 
                caption= caption, 
                url=upload_result.url, 
                file_type="video" if file.content_type.startswith("video/") else "image",  
                file_name=upload_result.name
            )

        session.add(post) 
        await session.commit() ## commit to the session to save it to the database
        await session.refresh(post) 
        return post 
        
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e)) 
    finally: 
        if temp_file_path and os.path.exists(temp_file_path): 
            os.unlink(temp_file_path) 
        file.file.close() 
        

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

@app.delete("/posts/{post_id}") 
async def delete_post(post_id: str, session:AsyncSession=Depends(get_async_session)): 
    try: 
        post_uuid=uuid.UUID(post_id) 
        result= await session.execute(select(Post).where(Post.id == post_uuid)) 
        
        post=result.scalars().first() 
        
        if not post: 
            raise HTTPException(status_code=404,detail="Post not found ") 
        
        await session.delete(post) 
        await session.commit() 
        return { "success":True, "message":"Post deleted successfully"}
    except Exception as e : 
        raise HTTPException(status_code=500,detail=str(e))