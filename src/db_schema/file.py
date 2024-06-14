from pydantic import BaseModel

class File(BaseModel):
    cn: str 
    dn: str
    isca: bool
    blob: str