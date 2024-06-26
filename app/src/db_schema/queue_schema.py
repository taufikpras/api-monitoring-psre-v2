from src.core.file_repo_core import find_file_from_file_id
from src.db_schema.crl_schema import CRL_Schema

class Queue_Schema():
    name:str
    url: str
    issuer_keyid: str
    issuer_dn: str
    user_file_pem: str=""
    issuer_file_pem: str=""
    hash=""
    
    def __init__(self, name:str,
                 url:str,
                 issuer_keyid:str,
                 issuer_dn:str) :
        self.name = name
        self.url = url
        self.issuer_dn = issuer_dn
        self.issuer_keyid = issuer_keyid
        
    @classmethod    
    def from_crl(cls,crl_schema:CRL_Schema):
        
        obj = cls(name="crl",
                   url=crl_schema.url,
                   issuer_keyid = crl_schema.issuer_keyid,
                   issuer_dn = crl_schema.issuer_dn)
        issuer_pem = find_file_from_file_id(crl_schema.issuer_file_id)
        obj.user_file_pem = issuer_pem
        
        return obj