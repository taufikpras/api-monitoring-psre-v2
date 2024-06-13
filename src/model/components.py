
class CA():
    id: str
    cn: str 
    dn: str
    keyid: str
    
class CRL():
    id: str
    url: str
    ca_filename:str

class OCSP():
    url: str
    user_file_name: str
    ca_file_name: str