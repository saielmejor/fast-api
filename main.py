import uvicorn # webserver 

if __name__ == "__main__":
    uvicorn.run("src.fastapi_tutorial.app:app", host="0.0.0.0", port=8000, reload=True)