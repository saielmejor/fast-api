from collections.abc import AsyncGenerator 
from datetime import datetime
import uuid 

from sqlalchemy import Column, String, Text,DateTime, ForeignKey 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine , async_sessionmaker 
from sqlalchemy.orm import  DeclarativeBase , relationship 


DATABASE_URL="sqlite+aiosqlite:///./test.db" 

class Base(DeclarativeBase): 
    pass

class Post (Base): 
    __tablename__= "posts" 
    id= Column (UUID(as_uuid=True),primary_key=True, default=uuid.uuid4) # create an id column 
    caption=Column(Text) 
    url=Column(String, nullable=False) 
    file_type=Column(String, nullable=False) 
    file_name=Column(String, nullable=False) 
    created_at=Column(DateTime,default=datetime.utcnow)



## create database 

engine=create_async_engine(DATABASE_URL) 
async_sessionmaker=async_sessionmaker(engine,expire_on_commit=False) 

async def create_db_and_tables():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) #find all the classes that it inherits and creates it in the database 

    
#creates a session 
async def get_async_session()-> AsyncGenerator[AsyncSession,None]: 
    async with async_sessionmaker() as session: 
        yield session
