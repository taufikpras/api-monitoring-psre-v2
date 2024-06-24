from pydantic import BaseModel
import datetime
import hashlib

class Tickets(BaseModel):
    uid: str
    start: datetime.datetime = None
    end: datetime.datetime | None = None
    last_notif: datetime.datetime | None = None
    cn: str
    url: str
    resolve: bool = False
    message: str 
    occurance: int = 1

class TicketsInput(BaseModel):
    ca_id:str
    cn:str
    obj_id:str
    message:str
    url: str

def create_uid(ca_id:str, object_id:str):
    uid_ = ca_id + object_id
    uid = hashlib.sha1(uid_.encode('utf-8')).hexdigest()

    return uid

def set_ticket_from_input(input:TicketsInput):
    uid_ = input.ca_id + input.obj_id
    uid = hashlib.sha1(uid_.encode('utf-8')).hexdigest()
    return Tickets(uid=uid,
              message=input.message,
              cn=input.cn,
              url=input.url,
              start=datetime.datetime.now())

def setTicket(ca_id:str, object_id:str, message:str, cn:str, url:str):
    uid_ = ca_id + object_id
    uid = hashlib.sha1(uid_.encode('utf-8')).hexdigest()
    return Tickets(uid=uid,
              message=message,
              cn=cn,
              url=url,
              start=datetime.datetime.now())

# def set_ticket_from
def to_object(dict_) -> Tickets:
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

def individual(objct) -> dict:
    
    if(objct != None):
        return{
            "id": str(objct["_id"]),
            "uid": str(objct["uid"]),
            "start": objct["start"].strftime("%Y-%m-%d %H:%M:%S"),
            "end": "" if objct["end"] is None else objct["end"].strftime("%Y-%m-%d %H:%M:%S"),
            "last_notif": "" if objct["last_notif"] is None else objct["last_notif"].strftime("%Y-%m-%d %H:%M:%S"),
            "message": str(objct["message"]),
            "cn": str(objct["cn"]),
            "url": str(objct["url"]),
            "occurance": int(objct["occurance"]),
            "resolve": bool(objct["resolve"])
        }
    else:
        return None

def list_serial(objcts) -> list:
    return[individual(objct) for objct in objcts]