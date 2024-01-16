from typing import Optional

from pydantic import BaseModel


class LineItem(BaseModel):
    name: str
    quantity: int
    rate: float
    total: float


class Earnings(BaseModel):
    """The calculated earnings"""
    line_items: list[LineItem]
    line_items_subtotal: Optional[float] = 0
    hours_worked: Optional[float] = 0
    minimum_earnings: Optional[float] = 0
    final_earnings: Optional[float] = 0
