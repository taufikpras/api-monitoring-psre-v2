from fastapi import APIRouter
import src.core.queue_core as queue_core

str_name = "verifier"
router = APIRouter(prefix="/api/"+str_name,tags=[str_name],)

@router.get("/crl_verifier")
async def crl_verifier():
    crls_q, ocsps_q = queue_core.get_all_queues()

    


    return {"crl":[crl_q.__dict__ for crl_q in crls_q],
            "ocsp":[ocsp_q.__dict__ for ocsp_q in ocsps_q]}