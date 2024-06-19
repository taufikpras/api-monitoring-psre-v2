
from src.model.crl import CRL_Model
from src.model.ocsp import OCSP_Model
import src.db_schema.ca as db_schema
from datetime import datetime
from src.model.cert import Cert_Model

class CA_Model():
    id: str = ""
    cn: str 
    dn: str
    keyid: str
    crls: list[CRL_Model] = []
    ocsps: list[OCSP_Model] = []

    def __eq__(self, other):
        if(other != None):
            return self.keyid == other.keyid
        else:
            return self.keyid == None

    def __init__(self,
                 cn: str,
                 dn:str,
                 keyid:str,
                 id:str="",
                 crls:list[CRL_Model]=[],
                 ocsps:list[OCSP_Model]=[]):
        self.cn = cn
        self.dn = dn
        self.keyid = keyid
        if(id != ""):
            self.id = id

        self.crls = crls 

        self.ocsps = ocsps 

def to_object_from_db(input:dict) -> CA_Model:
    if(input != None):
        return CA_Model(
            id = str(input["_id"]),
            cn = str(input["cn"]),
            dn = str(input["dn"]),
            keyid = str(input["keyid"]),
        )
    else:
        return None
    
def to_list_of_object_from_db(inputs:list[dict]) -> list[CA_Model]:
    return[to_object_from_db(input) for input in inputs]

def convert_to_schema(input:CA_Model) -> db_schema:
    if(input != None):
        return db_schema(cn=input.cn,
                        dn=input.dn,
                        keyid=input.keyid,
                        updated=datetime.now())
    else:
        return None
    
def create_ca_from_cert(cert_input: Cert_Model):
    if(cert_input != None):

        return CA_Model(cn=cert_input.cn,
                        dn=cert_input.dn,
                        keyid=cert_input.keyid)
    else:
        return None