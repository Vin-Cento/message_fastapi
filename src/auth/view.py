from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User_DB
from users.schema import User_Create
from .schema import Update_Username, Update_Password
from schema import Token
from utils import login_user, verify, create_access_token, hash

from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["Authentication"], prefix="")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup")
async def create_user(user: User_Create, db: Session = Depends(get_db)):
    # making sure username doesn't already exist
    # changing this code might effect login()
    does_exist = db.query(User_DB).filter(User_DB.username == user.username).first()
    if does_exist is None:
        user.password = hash(user.password)
        new_user = User_DB(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return Response(status_code=status.HTTP_200_OK)
    else:
        # unique_id has max of 4 characters
        unique_id: str = str(db.query(User_DB).count())[:4]
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User {user.username} already taken, try {user.username + unique_id}",
        )


@router.post("/login", response_model=Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # assuming username are unique
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
    return {"token": access_token}


@router.delete("/delete_account", status_code=status.HTTP_204_NO_CONTENT)
async def delect_account(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # assuming username are unique
    user = db.query(User_DB).filter(User_DB.username == user_credentials.username)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not verify(user_credentials.password, user.first().password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    user.delete(synchronize_session=False)
    db.commit()


@router.put("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user_input: Update_Password, db: Session = Depends(get_db), _=Depends(login_user)
):
    user = db.query(User_DB).filter(User_DB.username == user_input.username)
    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id:not found"
        )
    user.update({"password": hash(user_input.password_new)}, synchronize_session=False)
    db.commit()


@router.put("/reset_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username(
    user_input: Update_Username, db: Session = Depends(get_db), _=Depends(login_user)
):
    user = db.query(User_DB).filter(User_DB.username == user_input.username)
    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"username: {user_input.username} not found"
        )
    user_new= db.query(User_DB).filter(User_DB.username == user_input.username_new)
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
