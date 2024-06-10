from pydantic import BaseModel
import datetime


class CA(BaseModel):
    cn: str 
    dn: str
    keyid: str

def setCA(cn_:str, dn_:str, keyid_:str):
    return CA(cn=cn_,
              dn=dn_,
              keyid=keyid_)

def individual(objct) -> dict:
    if(objct != None):
        return{
            "id": str(objct["_id"]),
            "cn": str(objct["cn"]),
            "dn": str(objct["dn"]),
            "keyid": str(objct["keyid"]),
        }
    else:
        return None

def list_serial(objcts) -> list:
    return[individual(objct) for objct in objcts]