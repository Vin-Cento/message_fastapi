from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
from models import User_DB
from .schema import User_Create
from utils import hash

router = APIRouter(prefix="/users")


@router.post("/")
async def create_user(user: User_Create, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = User_DB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}")
async def read_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(User_DB).filter(User_DB.user_id == id)
    if user_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    return user_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User_DB).filter(User_DB.user_id == id)
    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
