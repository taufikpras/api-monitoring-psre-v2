

class OCSP_Model():
    id: str = ""
    url: str
    issuer_dn: str
    issuer_keyid: str
    subject_file_id: str
    issuer_file_id: str

    def __init__(self, url:str, issuer_dn:str, issuer_keyid:str, subject_file_id:str, issuer_file_id:str, id :str =""):
        if(id != ""):
            self.id = id
        self.url = url
        self.subject_file_id = subject_file_id
        self.issuer_dn = issuer_dn
        self.issuer_keyid = issuer_keyid
        self.issuer_file_id = issuer_file_id