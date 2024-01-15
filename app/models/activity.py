from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: Optional[str] = None
    route_id: str
    attempt_date_time: datetime
    success: bool
