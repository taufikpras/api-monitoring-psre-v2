
class CRL_Model():
    id: str = ""
    url: str
    issuer_dn: str
    issuer_keyid: str
    issuer_file_id:str

    def __init__(self, url:str, issuer_dn:str, issuer_keyid:str, issuer_file_id:str, id :str =""):
        self.url = url
        self.issuer_file_id = issuer_file_id
        if(id != ""):
            self.id = id
