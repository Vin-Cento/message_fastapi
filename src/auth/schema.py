from pydantic import BaseModel
from typing import Optional


# schema
class User(BaseModel):
    user_id: Optional[int]
    username: str
    password: str


class Update_Username(BaseModel):
    username: str
    password: str
    username_new: str


class Update_Password(BaseModel):
    username: str
    password: str
    password_new: str
