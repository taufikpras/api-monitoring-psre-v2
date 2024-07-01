from fastapi import APIRouter
from src.db_schema.queue_schema import Queue_Schema
from src.db_schema.verification_result_schema import Result_Schema, CRL_Result_Schema
from src.core import ticket_core

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

@router.get("/test_result_schema")
async def test_result_schema():
    res_sch = CRL_Result_Schema()

    res_sch.issuer_dn = "CN=Test CA - G1,O=Test,C=ID"
    res_sch.issuer_keyid = "AFJAK3RHHGT9S02492U0JJK"
    res_sch.url = "va.test.id/crl"
    res_sch.message.append("Availibility error")
    
    return res_sch.get_dict_result()

@router.get("/test_fail_result")
async def test_fail_result():
    res_sch = Result_Schema()

    res_sch.issuer_dn = "CN=Test CA - G1,O=Test,C=ID"
    res_sch.issuer_keyid = "AFJAK3RHHGT9S02492U0JJK"
    res_sch.url = "va.test.id/crl"
    res_sch.message.append("Availibility error")
    tick = ticket_core.log_ticket(res_sch)

    return tick.model_dump()

@router.get("/test_resolve")
async def test_resolve():
    res_sch = Result_Schema()

    res_sch.issuer_dn = "CN=Test CA - G1,O=Test,C=ID"
    res_sch.issuer_keyid = "AFJAK3RHHGT9S02492U0JJK"
    res_sch.url = "va.test.id/crl"
    res_sch.message.append("Availibility error")
    res_sch.overall = 1

    tick = ticket_core.log_ticket(res_sch)
    return tick.model_dump()
