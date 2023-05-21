from sqlalchemy import or_
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
    user_obj = (
        db.query(UserDB).filter(UserDB.username == passrequest_form.username).first()
    )
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(passrequest_form.password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials: no password",
        )
    access_token = create_access_token(data={"user_id": user_obj.user_id})
    return {"token": access_token}


@router.delete("/delete_account", status_code=status.HTTP_204_NO_CONTENT)
async def delect_account(
    passrequest_form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    _=Depends(login_user),
):
    users_select = db.query(UserDB).filter(UserDB.username == passrequest_form.username)
    user_obj = users_select.first()
    # check if username exist
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    # check if password works
    if not verify(passrequest_form.password, user_obj.password):  # type: ignore
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
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    users_select.update(
        {"password": hash(user_input.password_new)}, synchronize_session=False
    )
    db.commit()


@router.put("/reset_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(
    user_input: UpdateUsernameForm, db: Session = Depends(get_db), _=Depends(login_user)
):
    users_select = db.query(UserDB).filter(
        or_(
            UserDB.username == user_input.username,
            UserDB.username == user_input.username_new,
        )
    )
    user_obj, user_create_obj, id = None, None, 0
    for user in users_select.all():
        if user_input.username == user.username:
            user_obj = user
            id = user.user_id
        if user_input.username_new == user.username:
            user_create_obj = user
    # check if current username exist
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials",
        )
    # check if new username_new is new
    if user_create_obj is not None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"{user_input.username_new} already taken",
        )
    else:
        db.query(UserDB).filter(UserDB.user_id == id).update(
            {"username": user_input.username_new}, synchronize_session=False
        )
        db.commit()
