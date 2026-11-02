from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from .routers import orders, web
from .db import Base, engine
from . import models  # noqa: F401

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    logger.info("API de Órdenes iniciada")
    yield
    logger.info("API de Órdenes detenida")

app = FastAPI(lifespan=lifespan)

app.include_router(orders.router)
app.include_router(web.router)