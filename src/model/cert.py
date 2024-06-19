from src.db_schema.cert import Cert_Schema as db_schema
from datetime import datetime

class Cert_Model():
    id: str = ""
    subject_file_id: str
    issuer_file_id:str
    keyid: str
    cn: str 
    dn: str
    issuerdn:str
    issuercn:str
    isca: bool
    blob: str

    def __init__(self, subject_file_id:str, 
             issuer_file_id:str,
             cn:str,
             dn:str,
             isca:str,
             blob:str,
             keyid: str,
             issuerdn:str,
             issuercn:str,
             id:str = ""):
        self.subject_file_id = subject_file_id
        self.issuer_file_id = issuer_file_id
        self.cn = cn
        self.dn = dn
        self.keyid = keyid
        self.isca = isca
        self.blob = blob
        self.issuerdn = issuerdn
        self.issuercn = issuercn
        if(id != ""):
            self.id = id

def to_object_from_db(input:dict) -> Cert_Model:
    if(input != None):
        return Cert_Model(
            id = str(input["_id"]),
            cn = str(input["cn"]),
            dn = str(input["dn"]),
            issuerdn = str(input["issuerdn"]),
            issuercn = str(input["issuercn"]),
            subject_file_id = str(input["subject_file_id"]),
            issuer_file_id = str(input["issuer_file_id"]),
            keyid = str(input["keyid"]),
            isca = str(input["isca"]),
            blob = str(input["blob"])
        )
    else:
        return None
    
def to_list_of_object_from_db(inputs:list[dict]) -> list[Cert_Model]:
    return[to_object_from_db(input) for input in inputs]

def convert_to_schema(input:Cert_Model) -> db_schema:
    if(input != None):
        return db_schema(subject_file_id=input.subject_file_id,
                        issuer_file_id=input.issuer_file_id,
                        cn=input.cn,
                        dn=input.dn,
                        issuerdn=input.issuerdn,
                        issuercn=input.issuercn,
                        isca=input.isca,
                        blob=input.blob,
                        keyid=input.keyid,
                        updated=datetime.now())
    else:
        return None