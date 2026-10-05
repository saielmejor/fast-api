from pydantic import BaseModel   

class PostCreate(BaseModel): 
    title:str 
    content: str 
class PostResponse(BaseModel): # This is used for validation only  
    title:str 
    content: str 