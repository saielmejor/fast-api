from pydantic import BaseModel  
from fastapi_tutorial.users import schemas 
import uuid

class PostCreate(BaseModel): 
    title:str 
    content: str 
class PostResponse(BaseModel): # This is used for validation only  
    title:str 
    content: str 

class UserRead(schemas.BaseUser[uuid.UUID]): 
    pass

class UserCreate(schemas.BaseUSerCreate):
    pass 

class UserUpdate(schemas.BaseUserUpdate): 
    pass 