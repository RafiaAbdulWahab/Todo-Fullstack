from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware

from db import create_db_and_tables
from routes.tasks import router as tasks_router
from routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for managing the lifespan of the FastAPI application.
    Ensures database tables are created on startup.
    """
    print("Creating tables...")
    create_db_and_tables()
    print("Tables created!")
    yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
origins = ["*"] # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/")
def read_root():
    """
    Root endpoint for the FastAPI application.
    Returns a welcome message.
    """
    return {"message": "Welcome to the Todo Full-Stack Web Application Backend!"}
