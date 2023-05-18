
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session

from .models import Book_DB, Book

router = APIRouter(
    prefix="/books",
)

@router.post("/")
async def post_book(book: Book):
    print(book)
    return {"message": "success", "num": 1}


@router.get("/{id}")
async def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(Book_DB).filter(Book_DB.book_id == id).all()
