
from pydantic import BaseModel


class Earnings(BaseModel):
    """The calculated earnings"""
    total: int
