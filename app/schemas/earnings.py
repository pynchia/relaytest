
from pydantic import BaseModel


class LineItem(BaseModel):
    name: str
    quantity: int
    rate: float
    total: float


class Earnings(BaseModel):
    """The calculated earnings"""
    line_items: list[LineItem]
    line_items_subtotal: float
    hours_worked: float
    minimum_earnings: float
    final_earnings: float
