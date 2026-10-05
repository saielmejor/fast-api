from fastapi import FastAPI ,HTTPException, status, Depends, Response 

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
        "content": "This is my third post content"      
}
}
    
 
@app.get("/posts")
def get_all_posts():
    return text_posts 


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = text_posts.get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post