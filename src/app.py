from fastapi import FastAPI
import asyncio
from src.route.input import router as input_router


app = FastAPI()
app.include_router(input_router)