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


router = APIRouter(tags=["Authentication"], prefix="")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup")
async def create_user(user_new: SignupForm, db: Session = Depends(get_db)):
    try:
        user_new.password = hash(user_new.password)
        new_user = UserDB(**user_new.dict())
        db.add(new_user)
        db.flush()
    except IntegrityError:
        # unique_id has max of 4 characters
        db.rollback()
        unique_id: str = str(db.query(UserDB).count())[:4]
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User {user_new.username} already taken, try {user_new.username + unique_id}",
        )
    db.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/login", response_model=Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # assuming username are unique
    user = db.query(UserDB).filter(UserDB.username == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    access_token = create_access_token(data={"user_id": user.user_id})
    return {"token": access_token}


@router.delete("/delete_account", status_code=status.HTTP_204_NO_CONTENT)
async def delect_account(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # assuming username are unique
    user = db.query(UserDB).filter(UserDB.username == user_credentials.username)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(user_credentials.password, user.first().password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    user.delete(synchronize_session=False)
    db.commit()


@router.put("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user_input: UpdatePasswordForm, db: Session = Depends(get_db), _=Depends(login_user)
):
    user = db.query(UserDB).filter(UserDB.username == user_input.username)
    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id:not found"
        )
    user.update({"password": hash(user_input.password_new)}, synchronize_session=False)
    db.commit()


@router.put("/reset_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(
    user_input: UpdateUsernameForm, db: Session = Depends(get_db), _=Depends(login_user)
):
    user = db.query(UserDB).filter(UserDB.username == user_input.username)
    if user.first() == None:
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
        user.update({"username": user_input.username_new}, synchronize_session=False)
        db.commit()
