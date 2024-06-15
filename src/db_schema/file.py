from pydantic import BaseModel
from datetime import datetime

class File_Schema(BaseModel):
    subject_file_id: str
    issuer_file_id:str
    cn: str 
    dn: str
    isca: bool
    blob: str
    keyid: str
    updated: datetime = datetime.now()