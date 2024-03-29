import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.api.deps import get_db
from app import models, schemas
from app.crud import activity, earnings
from app.tiers import Tiers


router = APIRouter()


@router.post(
    "/{rate_card_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Earnings,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Message}},
)
async def calculate_earnings(
    *, db: Session = Depends(get_db), rate_card_id:Tiers, activity_log: list[models.Activity]
) -> schemas.Earnings:
    """
    Calculate earnings given an activity log
    """
    try:
        request_id = str(uuid.uuid1())
        await activity.add_log(db, request_id, activity_log)
        result_earnings = await earnings.calc_earnings(db, request_id, rate_card_id)
        await activity.delete_log(db, request_id)
        return result_earnings
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err.__dict__['orig'])
        )


# @router.post(
#     "/{rate_card_id}",
#     status_code=status.HTTP_201_CREATED,
# )
# async def calculate_earnings(
#     *, db: Session = Depends(get_db), rate_card_id:str, activity_log: list[str]
# ) -> str:
#     """
#     Calculate earnings given an activity log
#     """
#     return "Hello world"
