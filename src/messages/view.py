from fastapi import APIRouter, Depends, status, HTTPException, Response
from database import get_db
from sqlalchemy.orm import Session
from models import Message_DB
from utils import login_user
from .schema import Message


router = APIRouter(
    prefix="/api/v1/messages",
)


@router.post("")
async def create_message(
    message: Message,
    db: Session = Depends(get_db),
    _: int = Depends(login_user),
):
    new_message = Message_DB(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@router.get("")
async def read_message(db: Session = Depends(get_db), _: int = Depends(login_user)):
    message_query = (
        db.query(Message_DB).order_by(Message_DB.message_id.desc()).limit(10)
    )
    if message_query.first == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"message is empty"
        )
    return [
        {"message_id": message.message_id, "message": message.message}
        for message in message_query.all()
    ]


@router.get("/{id}")
async def read_message_id(id: int, db: Session = Depends(get_db)):
    message_query = db.query(Message_DB).filter(Message_DB.message_id == id)
    if message_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    return message_query.first()


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_message(id: int, message: Message, db: Session = Depends(get_db)):
    message_query = db.query(Message_DB).filter(Message_DB.message_id == id)
    if message_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    message_query.update({"message": message.message}, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: int, db: Session = Depends(get_db)):
    message = db.query(Message_DB).filter(Message_DB.message_id == id)
    if message.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    message.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
