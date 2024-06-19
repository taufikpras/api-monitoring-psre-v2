from pydantic import BaseModel
import datetime
from pydantic import Field
from bson import ObjectId 
from typing import Optional

class CA(BaseModel):
    cn: str 
    dn: str
    keyid: str
    updated: datetime = datetime.now()
