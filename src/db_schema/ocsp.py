from pydantic import BaseModel
import datetime

class OCSP(BaseModel):
    ca_id: str 
    last_check: datetime.datetime = datetime.datetime.now()
    url: str
    user_file_id: str
    ca_file_id: str