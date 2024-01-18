from typing import Callable
from fastapi import FastAPI
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import event

from app.api.api import api_router
from app.api import deps


TEST_DATABASE_URI = "sqlite://"  # in-memory db


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = FastAPI(title="Relaytest", openapi_url=None)
    # add_middlewares(app)
    app.include_router(api_router)
    return app


@pytest.fixture
def engine():
    """
    Provide a presteen clean DB
    """
    engine = create_engine(
        TEST_DATABASE_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    event.listen(engine, "connect", lambda c, _: c.execute("pragma foreign_keys=on"))
    SQLModel.metadata.create_all(engine)  # TODO here or ?
    return engine


@pytest.fixture
def db(engine) -> Session:
    with Session(engine) as session:
        yield session
        session.commit()  # TODO remove or use autocommit instead


@pytest.fixture
def test_get_db(db) -> Callable:
    def override_get_db():
        yield db

    return override_get_db


@pytest_asyncio.fixture
async def client(app: FastAPI, test_get_db):
    app.dependency_overrides[deps.get_db] = test_get_db
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac
