from collections.abc import AsyncGenerator 
from datetime import datetime
import uuid 

from sqlalchemy import Column, String, Text,DateTime, ForeignKey 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine , async_sessionmaker 
from sqlalchemy.orm import  DeclarativeBase , relationship 
from fastapi import Depends

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

DATABASE_URL="sqlite+aiosqlite:///./test.db" 

class Base(DeclarativeBase): 
    pass


class User(SQLAlchemyBaseUserTableUUID, Base) : 
    __allow_unmapped__ = True
    post= relationship( argument="Post", back_populates="user") 
    # Reference the id of the user 
class Post (Base): 
    __tablename__= "posts" 
    id= Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False )  # create an id column 
    caption=Column(Text) 
    url=Column(String, nullable=False) 
    file_type=Column(String, nullable=False) 
    file_name=Column(String, nullable=False) 
    created_at=Column(DateTime,default=datetime.utcnow)

    user= relationship(argument="User", back_populates="posts") # one to many relationship

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


async def get_user_db(session:AsyncSession=Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User) # get user database table 