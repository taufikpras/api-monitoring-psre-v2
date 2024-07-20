from fastapi import APIRouter
from src.core import ca_core, crl_core, ocsp_core
from src.db_schema.ca_schema import CA_Schema

str_name = "data"
router = APIRouter(prefix="/api/"+str_name,tags=[str_name],)

@router.get("/")
async def get(search_dn:str=None):
    if(search_dn != None):
        cas = ca_core.search_ca_by_dn(search_dn)
    else :
        cas = None
    list_cas = ca_core.get_all_ca_and_component(cas)
    dict_ = {}
    i=0
    for ca in list_cas:
        i+=1
        dict_[i] = ca
    return dict_

@router.get("/ca")
async def get(search_dn:str=None):
    if(search_dn != None):
        cas = ca_core.search_ca_by_dn(search_dn)
    else :
        cas = ca_core.get_all()
    
    dict_ = {}
    i=0
    for ca in cas:
        i+=1
        dict_[i] = ca
    return dict_
