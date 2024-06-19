from pydantic import BaseModel
from datetime import datetime

class OCSP(BaseModel):
    ca_id: str 
    updated: datetime = datetime.now()
    url: str
    user_file_id: str
    ca_file_id: str