

import requests
from src.db_schema.queue_schema import Queue_Schema
from src.util.cert_handler import read_cert_from_pem_str, get_is_ca, get_subject_dn, get_subject_cn
from cryptography.x509 import ocsp, Certificate
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
from timeit import default_timer as timer
from datetime import datetime

import logging
import src.parameters as param
logger = logging.getLogger(param.LOGGER_NAME)

class OCSP_verifier():
    availibility: int = 0
    verification: int = 0
    overall: int = 0
    response_time: int = 0
    content: dict = {}
    message: list[str] = []

    queue: Queue_Schema

    def __init__(self, queue: Queue_Schema):
        self.queue = queue
        self.message = []
        self.availibility = 0
        self.verification = 0
        self.overall = 0
        self.response_time = 0

        self.content = {}

    def create_ocsp_req(self,user_cert_pem:str, ca_cert_pem:str):
        user_cert = read_cert_from_pem_str(user_cert_pem)
        ca_cert = read_cert_from_pem_str(ca_cert_pem)
        builder = ocsp.OCSPRequestBuilder()
        builder = builder.add_certificate(user_cert, ca_cert, SHA256())
        req = builder.build()
        derOcspReq = req.public_bytes(serialization.Encoding.DER)

        return derOcspReq
    
    def request_ocsp(self):
        response = None
        logger.info("Start Check OCSP Availibility : "+self.queue.url)

        ocsp_req = self.create_ocsp_req(self.queue.user_file_pem, self.queue.issuer_file_pem)

        strtime = timer()
        try:
            data_ = requests.post(self.queue.url, data = ocsp_req, headers = {"Content-Type": "application/ocsp-request"})
            response = data_.content

        except Exception as err:
            logger.error("Connection Error : "+self.queue.url)
            self.message.append("Connection Error")
        finally:
            endtime = timer()
            self.response_time = endtime - strtime
            return response
        
    def verify_ocsp_cert(self, cert:Certificate):
        try:
            now_tz = datetime.now().astimezone()

            not_valid_after = cert.not_valid_after_utc.astimezone()
            if(not_valid_after < now_tz):
                logger.warning(get_subject_cn(cert)+ " is Expired",exc_info=True)
                return False
            else:
                return True
        except:
            logger.warning('unable to verify OCSP certificate : ' + get_subject_cn(cert),exc_info=True)
            return False

    def verify_ocsp(self, response):
        try:
            ocsp_resp = ocsp.load_der_ocsp_response(response)

            if(ocsp_resp != None and ocsp_resp.certificate_status):
                self.availability = 1
            else:
                self.message.append(f"OCSP Service Down {self.queue.url}")
            
            for cert in ocsp_resp.certificates:
                if(get_is_ca(cert) == False):
                    if(self.verify_ocsp_cert(cert) == True):
                        self.verification = 1
                    else:
                        self.message.append("OCSP Certificate Expired")
            
            if(self.availability == 1 and self.verification == 1):
                self.overall = 1
        except Exception as err:
            self.message.append("OCSP verification failed")
        


    
    def get_ocsp_content(self, response):
        try:
            ocsp_resp = ocsp.load_der_ocsp_response(response)
            self.content["status"] = str(ocsp_resp.response_status)
            self.content["hash"] = ocsp_resp.hash_algorithm.name

            chain = []
            for cert in ocsp_resp.certificates:
                chain.append(cert.subject.rfc4514_string())

            self.content["responder"] = chain
            self.content["thisUpdate"] = ocsp_resp.this_update.strftime("%Y-%m-%d %H:%M:%S") if ocsp_resp.this_update != None else ""
            self.content["nextUpdate"] = ocsp_resp.next_update.strftime("%Y-%m-%d %H:%M:%S") if ocsp_resp.next_update != None else ""

        
        except Exception as err:
            logger.error(err)
    
    def to_dict(self)-> dict:
        return {
            "queue" : self.queue.__dict__,
            "overall" : self.overall,
            "availibility" : self.availibility,
            "verification" : self.verification,
            "response_time" : self.response_time,
            "message" : self.message,
            "content" : self.content
        }
    
    def get_verification_result(self) -> dict:
        return {
            "overall" : self.overall,
            "availibility" : self.availibility,
            "verification" : self.verification,
            "response_time" : self.response_time
        }

    def get_ca_info(self) -> dict:
        return {
            "cn" : self.queue.issuer_cn,
            "dn" : self.queue.issuer_dn,
            "url" : self.queue.url
        }

    @classmethod
    def from_dict(cls,input:dict):
        queue = Queue_Schema.from_dict(input["queue"])

        obj = cls(queue)
        obj.overall = input["overall"]
        obj.availibility = input["availibility"]
        obj.verification = input["verification"]
        obj.response_time = input["response_time"]
        obj.message = input["message"]
        obj.content = input["content"]