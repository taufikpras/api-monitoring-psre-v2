from fastapi import FastAPI
import asyncio
from src.route.input_route import router as input_router
# from src.route.test import router as test_router
import src.logging as logging

logging.setup_loggers()
app = FastAPI()
app.include_router(input_router)
# app.include_router(test_router)
