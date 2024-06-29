from fastapi import APIRouter
import src.core.queue_core as queue_core
from src.util.crl_verifier import CRL_verifier
from src.util.ocsp_verifier import OCSP_verifier

str_name = "verifier"
router = APIRouter(prefix="/api/"+str_name,tags=[str_name],)

@router.get("/crl_verifier")
async def crl_verifier():
    crls_q = queue_core.create_crl_queues()
    res = []
    for crl in crls_q:
        verifier = CRL_verifier(crl)
        crl_data = verifier.request_crl()
        verifier.verify_crl(crldata=crl_data)
        verifier.get_crl_content(crl_data)
        res.append(verifier.to_dict())
    
    return res

@router.get("/ocsp_verifier")
async def ocsp_verifier():
    ocsps_q = queue_core.create_ocsp_queues()
    res = []
    for ocsp in ocsps_q:
        verifier = OCSP_verifier(ocsp)
        data = verifier.request_ocsp()
        verifier.verify_ocsp(data)
        verifier.get_ocsp_content(data)
        res.append(verifier.to_dict())
    
    return res