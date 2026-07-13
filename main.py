import uvicorn
from fastapi import FastAPI 
from sqlalchemy.orm import Session 
from auth import alchemy_model
from core.db import engine , Base
from auth.routes import router as auth_router

app = FastAPI(
    title="FastAPI Cofee shop",
    description="Creating Apis for Fastapi app - Aaish",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Database connected successfull🎉"}

app.include_router(auth_router)

alchemy_model.Base.metadata.create_all(bind=engine) # create connection with MYSQL

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

