import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.db import engine

logger = logging.getLogger(__name__)


async def get_db() -> Session:
    """
    Dependency function that yields db sessions
    """
    async with Session(engine) as session:
        try:
            yield session
            await session.commit()  # TODO remove or use autocommit instead
        except SQLAlchemyError:
            logger.error("Transaction failed, rolling back")
            await session.rollback()
            raise
