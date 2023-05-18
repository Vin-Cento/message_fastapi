from pydantic import BaseModel
from typing import Optional


# schema
class Message(BaseModel):
    message_id: Optional[int]
    message: str
