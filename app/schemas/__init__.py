from typing import Any

from pydantic import BaseModel

from .earnings import Earnings, LineItem


class Message(BaseModel):
    detail: str
