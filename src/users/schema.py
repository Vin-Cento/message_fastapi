from pydantic import BaseModel
from typing import Optional


class User_Create(BaseModel):
    user_id: Optional[int]
    username: str
    password: str
