from fastapi import FastAPI
import asyncio
from src.route.input_route import router as input_router
from src.route.test_route import router as test_router
from src.route.verfier_route import router as verfier_router
import src.logging as logging_
from src import parameters
import src.celery as celery
from fastapi_utils.tasks import repeat_every
import logging


logging_.setup_loggers()

logger = logging.getLogger(parameters.LOGGER_NAME)
app = FastAPI()
app.include_router(input_router)
app.include_router(test_router)
app.include_router(verfier_router)


@app.on_event("startup")
@repeat_every(seconds=180)  # 1 hour
async def repeated_task():
    logger.info("Executing verification task")
    celery.create_periodic_verification()
    logger.info("Done executing verification task")


