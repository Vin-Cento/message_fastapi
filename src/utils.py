from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWSError, jwt
from config import config

from schema import TokenData

SECRET_KEY: str | None = config["SECRET_KEY"]
ALGORITHM: str | None = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]

if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise Exception('ACCESS_TOKEN_EXPIRE_MINUTES is missing, edit .env')
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
if ALGORITHM is None:
    raise Exception('ALGORITHM is missing, edit .env')
if SECRET_KEY is None:
    raise Exception('SECRET_KEY is missing, edit .env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_token


def verify_access_token(token: str, credentials_expection):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        id = payload["user_id"]
        if id is None:
            raise credentials_expection
        tokendata = TokenData(id=id)
    except JWSError:
        raise credentials_expection
    return tokendata


def login_user(token: str = Depends(oauth2_scheme)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_expection)
