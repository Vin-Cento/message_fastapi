from pydantic import BaseModel
from typing import Optional


# schema
class UserForm(BaseModel):
    user_id: Optional[int]
    username: str
    password: str


class SignupForm(BaseModel):
    username: str
    password: str


class UpdateUsernameForm(BaseModel):
    username: str
    password: str
    username_new: str


class UpdatePasswordForm(BaseModel):
    username: str
    password: str
    password_new: str
