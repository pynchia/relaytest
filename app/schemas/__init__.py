from typing import Any

from pydantic import BaseModel

from .earnings import Earnings


class Message(BaseModel):
    detail: str
