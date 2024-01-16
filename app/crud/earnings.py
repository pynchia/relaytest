
from sqlmodel import Session, select

from app.schemas import Earnings, LineItem
from app.models import Activity
from app.tiers import Tiers


class BronzeEarnings:
    BRONZE_PER_SUCCESSFUL_ATTEMPT = 0.459
    BRONZE_PER_UNSUCCESSFUL_ATTEMPT = 0.229
    BRONZE_LONG_ROUTE_BONUS = 10.0
    BRONZE_LOYALTY_BONUS = 20.0

    def __init__(self):
        self.hourly_min_earnings = 14.50

    async def calc_earnings(self, db: Session, request_id: str):
        activities = db.exec(
            select(Activity).where(Activity.request_id == request_id)
        )
        return Earnings(
            line_items=[
                LineItem(
                    name=,
                    quantity=,
                    rate=self.BR,
                    total=
                )
            ]
        )


class SilverEarnings:
    SILVER_PER_SUCCESSFUL_ATTEMPT = 0.459
    SILVER_PER_UNSUCCESSFUL_ATTEMPT = 0.229
    SILVER_LONG_ROUTE_BONUS = 10.0
    SILVER_LOYALTY_BONUS = 20.0

    def __init__(self):
        self.hourly_min_earnings = 13.50

    async def calc_earnings(self, db: Session, request_id: str):
        activities = db.exec(
            select(Activity).where(Activity.request_id == request_id)
        )
        return Earnings(
            line_items=[
                LineItem(
                    name=,
                    quantity=,
                    rate=self.BR,
                    total=
                )
            ]
        )


class GoldEarnings:
    SILVER_PER_SUCCESSFUL_ATTEMPT = 0.459
    SILVER_PER_UNSUCCESSFUL_ATTEMPT = 0.229
    SILVER_LONG_ROUTE_BONUS = 10.0
    SILVER_LOYALTY_BONUS = 20.0

    def __init__(self):
        self.hourly_min_earnings = 15.0

    async def calc_earnings(self, db: Session, request_id: str):
        activities = db.exec(
            select(Activity).where(Activity.request_id == request_id)
        )
        return Earnings(
            line_items=[
                LineItem(
                    name=,
                    quantity=,
                    rate=self.BR,
                    total=
                )
            ]
        )


class PlatinumEarnings:
    SILVER_PER_SUCCESSFUL_ATTEMPT = 0.459
    SILVER_PER_UNSUCCESSFUL_ATTEMPT = 0.229
    SILVER_LONG_ROUTE_BONUS = 10.0
    SILVER_LOYALTY_BONUS = 20.0

    def __init__(self):
        self.hourly_min_earnings = 15.25

    async def calc_earnings(self, db: Session, request_id: str):
        activities = db.exec(
            select(Activity).where(Activity.request_id == request_id)
        )
        return Earnings(
            line_items=[
                LineItem(
                    name=,
                    quantity=,
                    rate=self.BR,
                    total=
                )
            ]
        )


class CRUDEarnings:
    def __init__(self):
        self.bronze = BronzeEarnings()
        self.silver = SilverEarnings()
        self.gold = GoldEarnings()
        self.platinum = PlatinumEarnings()

    async def calc_earnings(self, db: Session, request_id: str, tier:Tiers) -> Earnings:
        tier_instance = getattr(self, tier)
        earnings = await tier_instance.calc_earnings(db, request_id)  # find the instance for the calculation by name convention
        # now add the common attrs
        earnings.hours_worked = 12
        earnings.minimum_earnings = tier_instance.hourly_min_earnings*earnings.hours_worked
        return earnings
    

earnings = CRUDEarnings()
