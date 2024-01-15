from contextlib import asynccontextmanager

from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan():
    create_db_and_tables()
    yield


app = FastAPI(
    title="relaytest",
    description="a test",
    version="0.1.0",
    lifespan=lifespan
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8080"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(api_router)
