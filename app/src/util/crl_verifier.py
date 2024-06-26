import requests
import logging
from timeit import default_timer as timer

logger = logging.getLogger('monitoring_psre')

class CRL_verifier():
    availibility: int = 0
    validity: int = 0
    signature: int = 0
    time_delta: int = 0
    
    response_time: int = 0
    content: dict
    message: list[str]
    
    url: str
    user_cert_pem: str
    ca_cert_pem: str
    
    
    
    def request_crl(self, url: str):
        logger.info(f"Start Check CRL Availibility : {input['url']}")
        strtime = timer()

        try:
            logger.debug(f"start downloading : {input['url']}")
            response = requests.get(input["url"])
            logger.debug(response.status_code)
        except Exception as err:
            # logger.error("Connection Error : "+input["url"],exc_info=True)
            logger.error(f"Connection Error : {input['url']}",exc_info=True)
            message = "Unable to connect"

        endtime = timer()
        
    def verify_crl(self, crldata, ca_filename:str) -> bool:
        raise NotImplementedError

    def getCRLContent(crldata):
        raise NotImplementedError