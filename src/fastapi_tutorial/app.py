from fastapi import FastAPI ,HTTPException, status, Depends, Response 
from src.fastapi_tutorial.schemas import PostCreate , PostResponse

app=FastAPI() 

text_posts={
    # empty dictionary 
    1: {
        "title": "My first post",
        "content": "This is my first post content"
    }, 
    2: {
        "title": "My second post",
        "content": "This is my second post content"
    } ,
    3: {
        "title": "My third  post",
        "content": "This is my third post content"    , 
},
4: {
        "title": "My fourth  post",
        "content": "This is my third post content"      
}
}
    
 
@app.get("/posts") 
def get_all_posts(limit:int=None): 
    if limit:
        return list(text_posts.values())[:limit] # convert values into a list 
    # limit parameters is used tp limit show certain limit 
    return text_posts 


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = text_posts.get(post_id)
    if post_id not in post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post.get(post_id)

# Request body 

@app.post("/posts")

def create_post(post:PostCreate) -> PostResponse:  # add a validation when you sending the output 
    new_post={"title": post.title, "content":post.content}
    text_posts[max(text_posts.keys())+1]=new_post 
    return new_post