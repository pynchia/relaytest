
from sqlalchemy import func
from sqlalchemy.sql import text

from sqlmodel import Session, select

from app.schemas import Earnings, LineItem
from app.models import Activity
from app.tiers import Tiers


class BronzeEarnings:
    PER_SUCCESSFUL_ATTEMPT = 0.459
    PER_UNSUCCESSFUL_ATTEMPT = 0.229
    LONG_ROUTE_BONUS = 10.0
    LOYALTY_BONUS_ROUTES = 20.0

    def __init__(self):
        self.hourly_min_earnings = 14.50

    async def calc_earnings(self, db: Session, request_id: str):
        num_successful_activities = db.exec(
            select(func.count(Activity.id))
            .where(Activity.request_id==request_id)
            .where(Activity.success==True)
        ).one()

        num_unsuccessful_activities = db.exec(
            select(func.count(Activity.id))
            .where(Activity.request_id==request_id)
            .where(Activity.success==False)
        ).one()

        long_route_query = """
            SELECT route_id, count(id) as num
            FROM activity
            WHERE request_id = :request_id AND success = True
            GROUP BY route_id
            ORDER BY num DESC
        """
        longest_route_id, longest_route_num_drops = db.exec(
            text(long_route_query),
            params={
                'request_id': request_id,
            }
        ).first()

        num_distinct_routes_query = """
            SELECT count(DISTINCT route_id)
            FROM activity
            WHERE request_id = :request_id
        """
        num_distinct_routes, *_ = db.exec(
            text(num_distinct_routes_query),
            params={
                'request_id': request_id,
            }
        ).first()

        return Earnings(
            line_items=[
                LineItem(
                    name='Per successful attempt',
                    quantity=num_successful_activities,
                    rate=self.PER_SUCCESSFUL_ATTEMPT,
                    total=float(num_successful_activities)*self.PER_SUCCESSFUL_ATTEMPT
                ),
                LineItem(
                    name='Per unsuccessful attempt',
                    quantity=num_unsuccessful_activities,
                    rate=self.PER_UNSUCCESSFUL_ATTEMPT,
                    total=float(num_unsuccessful_activities)*self.PER_SUCCESSFUL_ATTEMPT
                ),
                LineItem(
                    name='Long route bonus',
                    quantity=1 if longest_route_num_drops>30 else 0,
                    rate=self.LONG_ROUTE_BONUS,
                    total=self.LONG_ROUTE_BONUS if longest_route_num_drops>30 else 0.0
                ),
                LineItem(
                    name='Loyalty bonus (routes)',
                    quantity=1 if num_distinct_routes>=10 else 0,
                    rate=self.LOYALTY_BONUS_ROUTES,
                    total=self.LOYALTY_BONUS_ROUTES if num_distinct_routes>=10 else 0.0
                ),
            ]
        )

# TODO implement the earnings for the remaining tiers
# Note: the main class is defined at the end of this module

    
# class SilverEarnings:
#     SILVER_PER_SUCCESSFUL_ATTEMPT = 0.459
#     SILVER_PER_UNSUCCESSFUL_ATTEMPT = 0.229
#     SILVER_LONG_ROUTE_BONUS = 10.0
#     SILVER_LOYALTY_BONUS = 20.0

#     def __init__(self):
#         self.hourly_min_earnings = 13.50

#     async def calc_earnings(self, db: Session, request_id: str):
#         activities = db.exec(
#             select(Activity).where(Activity.request_id == request_id)
#         )
#         return Earnings(
#             line_items=[
#                 LineItem(
#                     name=,
#                     quantity=,
#                     rate=self.BR,
#                     total=
#                 )
#             ]
#         )


# class GoldEarnings:
#     GOLD_PER_SUCCESSFUL_ATTEMPT = 0.459
#     GOLD_PER_UNSUCCESSFUL_ATTEMPT = 0.229
#     GOLD_LONG_ROUTE_BONUS = 10.0
#     GOLD_LOYALTY_BONUS = 20.0

#     def __init__(self):
#         self.hourly_min_earnings = 15.0

#     async def calc_earnings(self, db: Session, request_id: str):
#         activities = db.exec(
#             select(Activity).where(Activity.request_id == request_id)
#         )
#         return Earnings(
#             line_items=[
#                 LineItem(
#                     name=,
#                     quantity=,
#                     rate=self.BR,
#                     total=
#                 )
#             ]
#         )


# class PlatinumEarnings:
#     PLATINUM_PER_SUCCESSFUL_ATTEMPT = 0.459
#     PLATINUM_PER_UNSUCCESSFUL_ATTEMPT = 0.229
#     PLATINUM_LONG_ROUTE_BONUS = 10.0
#     PLATINUM_LOYALTY_BONUS = 20.0

#     def __init__(self):
#         self.hourly_min_earnings = 15.25

#     async def calc_earnings(self, db: Session, request_id: str):
#         activities = db.exec(
#             select(Activity).where(Activity.request_id == request_id)
#         )
#         return Earnings(
#             line_items=[
#                 LineItem(
#                     name=,
#                     quantity=,
#                     rate=self.BR,
#                     total=
#                 )
#             ]
#         )


class CRUDEarnings:
    def __init__(self):
        # use composition for each tier
        self.bronze_tier = BronzeEarnings()
        # self.silver_tier = SilverEarnings()
        # self.gold_tier = GoldEarnings()
        # self.platinum_tier = PlatinumEarnings()

    async def calc_earnings(self, db: Session, request_id: str, tier:Tiers) -> Earnings:
        tier_instance = getattr(self, tier)  # find the instance for the calculation by name convention
        earnings = await tier_instance.calc_earnings(db, request_id)
        # now add the common attrs
        earnings.hours_worked = 12
        earnings.minimum_earnings = tier_instance.hourly_min_earnings*earnings.hours_worked
        earnings.final_earnings = earnings.line_items_subtotal + earnings.minimum_earnings

        return earnings
   

earnings = CRUDEarnings()
