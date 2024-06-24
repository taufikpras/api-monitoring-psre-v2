from pydantic import BaseModel
from datetime import datetime

class OCSP_Schema(BaseModel):
    updated: datetime = datetime.now()
    url: str
    issuer_keyid: str
    issuer_dn: str
    user_file_id: str
    issuer_file_id: str