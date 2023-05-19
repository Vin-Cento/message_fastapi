from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    id: Optional[int]
