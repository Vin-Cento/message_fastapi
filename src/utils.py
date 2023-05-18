from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWSError, jwt

from schema import TokenData

SECRET_KEY = "e461005220398152091142c3bdc709cde98651b6356c6afd94b42305d7d72392"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
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
        print(id)
        if id is None:
            raise credentials_expection
        tokendata = TokenData(id=id)
    except JWSError:
        raise credentials_expection
    return tokendata


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_expection)
