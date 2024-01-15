import uuid

from sqlalchemy.sql import text

from app import models, schemas
# from app.crud.base import CRUDBase


class CRUDActivity:
    async def add_log(db, request_id: uuid.UUID, activity_log: list[schemas.ActivityCreate]):
        ins_query = """
            INSERT INTO public.activity (request_id, route_id, attempt_date_time, success)
            VALUES (:request_id, :route_id, :attempt_date_time, :success)
        """
        await db.execute(
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
        await db.commit()


activity = CRUDActivity()
