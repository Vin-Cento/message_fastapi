from models import UserDB

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from .schema import UpdateUsernameForm, UpdatePasswordForm, SignupForm

from schema import Token
from fastapi.security import OAuth2PasswordBearer

from database import get_db
from utils import login_user, verify, create_access_token, hash

import random

random.seed()


router = APIRouter(tags=["Authentication"], prefix="")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup")
async def create_user(signup_form: SignupForm, db: Session = Depends(get_db)):
    try:
        signup_form.password = hash(signup_form.password)
        user_obj = UserDB(**signup_form.dict())
        db.add(user_obj)
        db.flush()
    except IntegrityError:
        db.rollback()
        unique_usernames: str = str(
            [signup_form.username + str(random.randint(0, 99)) for _ in range(4)]
        )
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"{signup_form.username} taken, try {unique_usernames}",
        )
    db.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/login", response_model=Token)
async def login(
    passrequest_form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # assuming username are unique
    user_obj = db.query(UserDB).filter(UserDB.username == passrequest_form.username).first()
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(passrequest_form.password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials: no password"
        )
    access_token = create_access_token(data={"user_id": user_obj.user_id})
    return {"token": access_token}


@router.delete("/delete_account", status_code=status.HTTP_204_NO_CONTENT)
async def delect_account(
    passrequest_form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # assuming username are unique
    users_select = db.query(UserDB).filter(UserDB.username == passrequest_form.username)
    user_obj = users_select.first()
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(passrequest_form.password, users_select.first().password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    users_select.delete(synchronize_session=False)
    db.commit()


@router.put("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user_input: UpdatePasswordForm, db: Session = Depends(get_db), _=Depends(login_user)
):
    users_select = db.query(UserDB).filter(UserDB.username == user_input.username)
    user_obj = users_select.first()
    if user_obj == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id:not found"
        )
    users_select.update({"password": hash(user_input.password_new)}, synchronize_session=False)
    db.commit()


@router.put("/reset_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(
    user_input: UpdateUsernameForm, db: Session = Depends(get_db), _=Depends(login_user)
):
    users_select = db.query(UserDB).filter(UserDB.username == user_input.username)
    user_obj = users_select.first()
    if user_obj == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"username: {user_input.username} not found",
        )
    user_new = db.query(UserDB).filter(UserDB.username == user_input.username_new)
    # TODO: make this one query
    # check if the new username_new is taken or not
    if user_new.first() == None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User {user_input.username_new} already taken",
        )
    else:
        users_select.update({"username": user_input.username_new}, synchronize_session=False)
        db.commit()
