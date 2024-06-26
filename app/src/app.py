from fastapi import FastAPI
import asyncio
from src.route.input_route import router as input_router
from src.route.test_route import router as test_router
from src.route.verfier_route import router as verfier_router
import src.logging as logging

logging.setup_loggers()
app = FastAPI()
app.include_router(input_router)
app.include_router(test_router)
app.include_router(verfier_router)
