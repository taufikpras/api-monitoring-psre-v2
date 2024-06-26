from fastapi import APIRouter
from src.db_schema.queue_schema import Queue_Schema

str_name = "test"
router = APIRouter(prefix="/api/"+str_name,tags=[str_name],)

@router.get("/")
async def get():
    obj = Queue_Schema()
    obj.name = "crl"
    obj.issuer_dn = "cn=a,c=id"
    obj.issuer_cn = "a"
    obj.url = "crl.a.id"
    obj.issuer_keyid = "asda223sdsfn"

    obj2 = Queue_Schema.from_dict(obj.__dict__)
    return obj2.__dict__