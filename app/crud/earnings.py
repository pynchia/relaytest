
from sqlmodel import Session, select

from app import schemas
from app.models import Activity
from app.tiers import Tiers


class CRUDEarnings:
    def __init__(self):
        self.tiers_min_earnings = {
            Tiers.bronze: 14.50,
            Tiers.silver: 13.50,
            Tiers.gold: 15.0,
            Tiers.platinum: 15.25,
        }

    BRONZE_PER_SUCCESSFUL_ATTEMPT = 0.459
    BRONZE_PER_UNSUCCESSFUL_ATTEMPT = 0.229
    BRONZE_LONG_ROUTE_BONUS = 10.0
    BRONZE_LOYALTY_BONUS = 20.0


    async def calc_earnings(self, db: Session, request_id: str, tier:Tiers) -> schemas.Earnings:
        earnings = await getattr(self, 'calc_'+tier)(db, request_id)  # map by name convention
        # now add the common attrs
        earnings.hours_worked = 12
        earnings.minimum_earnings = self.tiers_min_earnings[tier]
        return earnings
    
    async def calc_bronze(self, db: Session, request_id: str):
        activities = db.exec(
            select(Activity).where(Activity.request_id == request_id)
        )
        return schemas.Earnings(

        )

    async def calc_silver(self, db: Session, request_id: str):
        return schemas.Earnings(
            
        )

    async def calc_gold(self, db: Session, request_id: str):
        return schemas.Earnings(
            
        )

    async def calc_platinum(self, db: Session, request_id: str):
        return schemas.Earnings(
            
        )


earnings = CRUDEarnings()
