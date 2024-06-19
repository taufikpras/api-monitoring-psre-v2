from pydantic import BaseModel
from datetime import datetime


class CRL(BaseModel):
    ca_id: str 
    updated: datetime = datetime.now()
    url: str
    ca_file_id:str