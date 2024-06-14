from pydantic import BaseModel

class File(BaseModel):
    subject_file_id: str
    issuer_file_id:str
    cn: str 
    dn: str
    isca: bool
    blob: str