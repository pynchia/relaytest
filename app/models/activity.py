from datetime import datetime

from sqlmodel import Field, SQLModel


class Activity(SQLModel, table=True):
    request_id: str = Field(..., primary_key=True)
    route_id: str = Field(index=True)
    attempt_date_time: datetime
    success: bool
