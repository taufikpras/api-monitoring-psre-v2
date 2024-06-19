from pydantic import BaseModel
from datetime import datetime

class Cert_Schema(BaseModel):
    subject_file_id: str
    issuer_file_id:str
    cn: str 
    dn: str
    issuerdn: str
    issuercn:str
    isca: bool
    blob: str
    keyid: str
    updated: datetime = datetime.now()