from src.db_schema.ca_schema import CA_Schema
from src.db_schema.crl_schema import CRL_Schema
from src.db_schema.ocsp_schema import OCSP_Schema
from src.db_schema.ca_component_schema import CA_Component_Schema
from src.db_schema.file_repo_schema import File_Repo_Schema
from src.db_schema.queue_schema import Queue_Schema
from src.core import ca_core, file_repo_core

import logging
import src.parameters as param

logger = logging.getLogger(param.LOGGER_NAME)

def create_queues_from_ca(ca:CA_Schema, crls:list[CRL_Schema], ocsps:list[OCSP_Schema]):
    crl_queues = []
    ocsp_queues = []

    for crl in crls:
        queue = Queue_Schema()
        queue.name = "crl"
        queue.url = crl.url
        queue.issuer_keyid = crl.issuer_keyid
        queue.issuer_dn = crl.issuer_dn
        queue.issuer_cn = ca.cn
        queue.issuer_file_pem = file_repo_core.find_file_from_file_id(crl.issuer_file_id).blob

        crl_queues.append(queue)
    
    for ocsp in ocsps:
        queue = Queue_Schema()
        queue.name = "ocsp"
        queue.url = ocsp.url
        queue.issuer_keyid = ocsp.issuer_keyid
        queue.issuer_dn = ocsp.issuer_dn
        queue.issuer_cn = ca.cn
        queue.issuer_file_pem = file_repo_core.find_file_from_file_id(ocsp.issuer_file_id).blob
        queue.user_file_pem = file_repo_core.find_file_from_file_id(ocsp.user_file_id).blob

        ocsp_queues.append(queue)
    
    return crl_queues, ocsp_queues

def get_all_queues() -> tuple[list[Queue_Schema],list[Queue_Schema]]:
    ca_components:list[CA_Component_Schema] = []
    crls_queues = []
    ocsps_queues = []
    ca_components = ca_core.get_all_ca_and_component()

    for ca_component in ca_components:
        crls_queues_, ocsps_queues_ = create_queues_from_ca(ca_component.ca,ca_component.crls, ca_component.ocsps)
        crls_queues = crls_queues + crls_queues_
        ocsps_queues = ocsps_queues + ocsps_queues_
    
    return crls_queues, ocsps_queues

def create_crl_queues()


    

    