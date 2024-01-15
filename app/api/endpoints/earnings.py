import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import activity, earnings, Tiers
from app.exceptions import ModelNotFoundException
from app.schemas import Activity, ActivityCreate, Earnings, Message


router = APIRouter()


@router.post(
    "/{rate_card_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=Earnings,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}},
)
async def calculate_earnings(
    *, db: AsyncSession = Depends(get_db), rate_card_id:Tiers, activity_log: list[ActivityCreate]
) -> Activity:
    """
    Calculate earnings given an activity log
    """
    return "Hello world"

    try:
        request_id = uuid.uuid1()
        await activity.add_log(db, request_id, activity_log)
        return await earnings.calc_earnings(request_id, rate_card_id)
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err.__dict__['orig'])
        )