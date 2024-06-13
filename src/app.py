from fastapi import FastAPI
import asyncio
from src.route.ca import router as ca_router


app = FastAPI()
app.include_router(ca_router)