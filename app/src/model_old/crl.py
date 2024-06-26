from datetime import datetime
from src.db_schema.crl_schema import CRL as db_schema


class CRL_Model():
    id: str = ""
    url: str
    issuer_dn: str
    issuer_keyid: str
    issuer_file_id:str

    def __init__(self, url:str, issuer_dn:str, issuer_keyid:str, issuer_file_id:str, id :str =""):
        self.url = url
        self.issuer_file_id = issuer_file_id
        self.issuer_keyid = issuer_keyid
        self.issuer_dn = issuer_dn
        if(id != ""):
            self.id = id
    
def to_object_from_db(input:dict) -> CRL_Model:
    if(input != None):
        return CRL_Model(
            id = str(input["_id"]),
            url = str(input["url"]),
            issuer_dn = str(input["issuer_dn"]),
            issuer_keyid = str(input["issuer_keyid"]),
            issuer_file_id = str(input["issuer_file_id"]),
        )
    else:
        return None
    
def to_list_of_object_from_db(inputs:list[dict]) -> list[CRL_Model]:
    return[to_object_from_db(input) for input in inputs]

def convert_to_schema(input:CRL_Model) -> db_schema:
    if(input != None):
        return db_schema(cn=input.cn,
                        dn=input.dn,
                        keyid=input.keyid,
                        updated=datetime.now())
    else:
        return None
