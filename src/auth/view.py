from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User_DB
from .schema import Update_Username, Update_Password
from utils import verify, create_access_token

from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["Authentication"], prefix="")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # what to do when username are the same
    user = (
        db.query(User_DB).filter(User_DB.username == user_credentials.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    access_token = create_access_token(data={"user_id": user.user_id})
    print(access_token)
    return {"token": access_token}


@router.put("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    id: int, user: Update_Password, db: Session = Depends(get_db)
):
    test_query = db.query(User_DB).filter(User_DB.user_id == id)
    if test_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    test_query.update({"password": hash(user.password)}, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/reset_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(
    id: int, user: Update_Username, db: Session = Depends(get_db)
):
    test_query = db.query(User_DB).filter(User_DB.user_id == id)
    if test_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found"
        )
    test_query.update({"username": user.username}, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
