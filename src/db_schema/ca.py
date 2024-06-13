from pydantic import BaseModel
import datetime
from pydantic import Field
from bson import ObjectId 
from typing import Optional

class CA(BaseModel):
    cn: str 
    dn: str
    keyid: str

def setCA(cn_:str, dn_:str, keyid_:str):
    return CA(cn=cn_,
              dn=dn_,
              keyid=keyid_)


def to_object(objct) -> CA:
    if(objct != None):
        return CA(
            id = ObjectId(objct["_id"]),
            cn = str(objct["cn"]),
            dn = str(objct["dn"]),
            keyid = str(objct["keyid"]),
        )
    else:
        return None

def list_object(objcts) -> list[CA]:
    return[to_object(objct) for objct in objcts]



def to_dict(objct:CA) -> dict:
    if(objct != None):
        return{
            "id": str(objct.id),
            "cn": objct.cn,
            "dn": objct.dn,
            "keyid": objct.keyid,
        }
    else:
        return None

def list_dict(objcts) -> list[dict]:
    return[to_dict(objct) for objct in objcts]