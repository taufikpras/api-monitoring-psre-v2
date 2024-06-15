from fastapi import FastAPI
import asyncio
from src.route.input import router as input_router
import src.logging as logging

logging.setup_loggers()
app = FastAPI()
app.include_router(input_router)
