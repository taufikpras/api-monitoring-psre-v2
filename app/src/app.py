from fastapi import FastAPI
import asyncio
from src.route.input_route import router as input_router
from src.route.test_route import router as test_router
from src.route.verfier_route import router as verfier_router
from src.route.data_route import router as data_router
import src.logging as logging_
from src import parameters as params
import src.celery as celery
from fastapi_utils.tasks import repeat_every
import logging


logging_.setup_loggers()

logger = logging.getLogger(params.LOGGER_NAME)
app = FastAPI()
app.include_router(input_router)
app.include_router(data_router)
app.include_router(verfier_router)
app.include_router(test_router)


@repeat_every(seconds=params.TIME_INTERVAL)  # 1 hour
async def repeated_task():
    logger.info("Executing verification task")
    celery.create_periodic_verification()
    logger.info("Done executing verification task")
    
    logger.info("Send Notfication Task")
    num = celery.verifier_notification()
    logger.info(f"{num} Notifications found")
    logger.info("Done Sending Notfication Task")

@app.on_event("startup")
async def startup_event():
    await repeated_task()

