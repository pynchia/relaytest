import uuid

from sqlalchemy.sql import text
from sqlmodel import Session

from app import models
# from app.crud.base import CRUDBase


class CRUDActivity:
    async def add_log(db: Session, request_id: uuid.UUID, activity_log: list[models.Activity]):
        ins_query = """
            INSERT INTO public.activity (request_id, route_id, attempt_date_time, success)
            VALUES (:request_id, :route_id, :attempt_date_time, :success)
        """
        db.exec(
            text(ins_query),
            [
                {
                    'request_id': request_id,
                    'route_id': ac.route_id,
                    'attempt_date_time': ac.attempt_date_time,
                    'success': ac.success
                }
                for ac in activity_log
            ]
        )
        db.commit()


activity = CRUDActivity()
