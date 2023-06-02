from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from database import engine

from sqlalchemy.ext.declarative import declarative_base

from messages import view as messages
from auth import view as auth
# from books import view as book

Base = declarative_base()
# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Censustract API by Vincent Liu"}


app.include_router(messages.router)
app.include_router(auth.router)
