from src.db_schema.file import File_Schema as db_schema
from datetime import datetime

class File():
    id: str = ""
    subject_file_id: str
    issuer_file_id:str
    keyid: str
    cn: str 
    dn: str
    isca: bool
    blob: str

    def __init__(self, subject_file_id:str, 
             issuer_file_id:str,
             cn:str,
             dn:str,
             isca:str,
             blob:str,
             keyid: str,
             id:str = ""):
        self.subject_file_id = subject_file_id
        self.issuer_file_id = issuer_file_id
        self.cn = cn
        self.dn = dn
        self.keyid = keyid
        self.isca = isca
        self.blob = blob
        if(id != ""):
            self.id = id

def to_object_from_db(input:dict) -> File:
    if(input != None):
        return File(
            id = str(input["_id"]),
            cn = str(input["cn"]),
            dn = str(input["dn"]),
            subject_file_id = str(input["subject_file_id"]),
            issuer_file_id = str(input["issuer_file_id"]),
            keyid = str(input["keyid"]),
            isca = str(input["isca"]),
            blob = str(input["blob"])
        )
    else:
        return None
    
def to_list_of_object_from_db(inputs:list[dict]) -> list[File]:
    return[to_object_from_db(input) for input in inputs]

def convert_to_schema(input:File) -> db_schema:
    if(input != None):
        return db_schema(subject_file_id=input.subject_file_id,
                        issuer_file_id=input.issuer_file_id,
                        cn=input.cn,
                        dn=input.dn,
                        isca=input.isca,
                        blob=input.blob,
                        keyid=input.keyid,
                        updated=datetime.now())
    else:
        return None