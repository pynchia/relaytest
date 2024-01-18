
from sqlalchemy.sql import text
from sqlmodel import Session

from app import models
# from app.crud.base import CRUDBase


class CRUDActivity:
    @staticmethod
    async def add_log(db: Session, request_id: str, activity_log: list[models.Activity]):
        """
        Add the activities (drops) to the DB
        """
        ins_query = """
            INSERT INTO activity (request_id, route_id, attempt_date_time, success)
            VALUES (:request_id, :route_id, :attempt_date_time, :success)
        """
        db.exec(
            text(ins_query),
            params=[
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

    @staticmethod
    async def delete_log(db: Session, request_id: str):
        """
        Remove the activities (drops) from the DB
        """
        delete_query = """
            DELETE FROM activity
            WHERE request_id = :request_id
        """
        db.exec(
            text(delete_query),
            params={
                'request_id': request_id,
            }
        )
        db.commit()

activity = CRUDActivity()
