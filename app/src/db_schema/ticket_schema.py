from pydantic import BaseModel
import datetime
import hashlib


class Tickets_Schema(BaseModel):
    uid: str
    start: datetime.datetime = None
    end: datetime.datetime | None = None
    last_notif: datetime.datetime | None = None
    cn: str
    url: str
    resolve: bool = False
    message: str 
    occurance: int = 1

def create_uid(issuer_keyid:str,url:str, issuer_dn:str):
    uid_ = issuer_dn + issuer_keyid + url
    uid = hashlib.sha1(uid_.encode('utf-8')).hexdigest()

    return uid

def __init__(self, issuer_keyid, issuer_dn, issuer_cn, url, message):
    self.uid = create_uid(issuer_keyid, url, issuer_dn)
    self.cn = issuer_cn
    self.url = url
    self.message = message


def setTicket(ca_id:str, object_id:str, message:str, cn:str, url:str):
    uid_ = ca_id + object_id
    uid = hashlib.sha1(uid_.encode('utf-8')).hexdigest()
    return Tickets(uid=uid,
              message=message,
              cn=cn,
              url=url,
              start=datetime.datetime.now())

# def set_ticket_from
def to_object_from_db(dict_) -> Tickets:
    print(dict_)
    return Tickets(
        uid=dict_["uid"],
        message=dict_["message"],
        cn=dict_["cn"],
        url=dict_["url"],
        resolve=dict_["resolve"],
        occurance=dict_["occurance"],
        end= None if dict_["end"] == "" else datetime.datetime.strptime(dict_["end"],"%Y-%m-%d %H:%M:%S"),
        start=datetime.datetime.strptime(dict_["start"],"%Y-%m-%d %H:%M:%S"),
        last_notif= None if dict_["last_notif"] == "" else datetime.datetime.strptime(dict_["last_notif"],"%Y-%m-%d %H:%M:%S")
    )

def to_list_of_object_from_db(objcts) -> list:
    return[to_object_from_db(objct) for objct in objcts]