import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import auth, boards, tasks, stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskBoard Lite API",
    description="Προσωπικός Διαχειριστής Tasks με Kanban Board",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(boards.router)
app.include_router(tasks.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "TaskBoard Lite API is running!"}