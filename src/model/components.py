
class CRL():
    id: str = ""
    url: str
    issuer_file_id:str

    def __init__(self, url:str, issuer_file_id:str, id :str =""):
        self.url = url
        self.issuer_file_id = issuer_file_id
        if(id != ""):
            self.id = id

class OCSP():
    id: str = ""
    url: str
    subject_file_id: str
    issuer_file_id: str

    def __init__(self, url:str, subject_file_id:str, issuer_file_id:str, id :str =""):
        if(id != ""):
            self.id = id
        self.url = url
        self.subject_file_id = subject_file_id
        self.issuer_file_id = issuer_file_id


class File():
    id: str = ""
    subject_file_id: str
    issuer_file_id:str
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
             id:str = ""):
        self.subject_file_id = subject_file_id
        self.issuer_file_id = issuer_file_id
        self.cn = cn
        self.dn = dn
        self.isca = isca
        self.blob = blob
        if(id != ""):
            self.id = id

class CA():
    id: str = ""
    cn: str 
    dn: str
    keyid: str
    crls: list[CRL] = []
    ocsps: list[OCSP] = []

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
                 crls:list[CRL]=[],
                 ocsps:list[OCSP]=[]):
        self.cn = cn
        self.dn = dn
        self.keyid = keyid
        if(id != ""):
            self.id = id

        self.crls = crls 

        self.ocsps = ocsps 