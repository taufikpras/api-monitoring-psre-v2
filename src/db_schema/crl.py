from pydantic import BaseModel
import datetime


class CRL(BaseModel):
    ca_id: str 
    last_check: datetime.datetime = datetime.datetime.now()
    url: str
    ca_filename:str