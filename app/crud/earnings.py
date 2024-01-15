import uuid

from app import models, schemas
from app.tiers import Tiers


class CRUDEarnings:
    @staticmethod
    async def calc_earnings(request_id: uuid.UUID, rate_card_id:Tiers) -> schemas.Earnings:
        total = 123
        return schemas.Earnings(
            total=total
        )


earnings = CRUDEarnings()
