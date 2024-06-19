import hashlib
import os
from src.model.ca import CA_Model
from src.model.crl import CRL_Model
from src.model.ocsp import OCSP_Model
import src.util.cert_handler as cert_handler
import zipfile
import shutil
import pathlib
import src.parameters as param
import logging
from cryptography.x509.base import Certificate
from src.model.cert import Cert_Model 
import src.core.cert as cert_core 

logger = logging.getLogger('monitoring_psre')



def read_file_input(path=param.TEMP, res:list=[]):
    # res = []
    for path_ in os.listdir(path):
        # check if current path is a file
        if os.path.isfile(os.path.join(path, path_)):
            # print(os.path.join(path, path_))
            res.append(os.path.join(path, path_))
        else:
            read_file_input(os.path.join(path,path_), res)
    return res


def get_input_path(filename:str):
    if(filename.startswith(param.INPUT_PATH)):
        return filename
    else:
        return os.path.join(param.INPUT_PATH,filename)

def getDataPath(filename:str):
    if(filename.startswith(param.DATA_PATH)):
        return filename
    else:
        return os.path.join(param.DATA_PATH,filename)
    
    
def create_file_id(cert: Certificate):
    string_input = cert_handler.get_subject_dn(cert)+"-"+str(cert_handler.get_subject_key_identifier(cert))
    filename = hashlib.sha1(string_input.encode()).hexdigest()
    return filename

def create_issuer_file_id(cert: Certificate):
    string_input = cert_handler.get_issuer_dn(cert)+"-"+str(cert_handler.get_authorithy_key_identifier(cert))
    filename = hashlib.sha1(string_input.encode()).hexdigest()
    return filename

def parse_ca_from_file(cert:Cert_Model) -> CA_Model:
    crls:list[CRL_Model] = []
    ocsps:list[OCSP_Model] = []
    ca: CA_Model = None
    
    try:

        issuer_cert = cert_core.find_file_from_file_id(cert.issuer_file_id)
        if(issuer_cert != None):
            cert_ = cert_handler.read_cert_from_pem_str(cert.blob)
            crl_urls = cert_handler.get_crls(cert_)
            ocsp_urls = cert_handler.get_ocsps(cert_)

            for crl_url in crl_urls:
                crls.append(CRL_Model(url=crl_url, issuer_file_id=cert.issuer_file_id))
            
            for ocsp_url in ocsp_urls:
                ocsps.append(OCSP_Model(url=ocsp_url,subject_file_id=cert.subject_file_id, issuer_file_id=cert.issuer_file_id))
            
            ca = CA_Model(cn=cert.cn, dn=cert.dn, keyid=cert.keyid, crls=crls, ocsps=ocsps)

            return ca
        else:
            logger.warning(f"Unable Find Issuer Cert with DN : {cert.issuerdn}")
            return None
    except Exception as e:
        logger.error(e, exc_info=True)

def parse_file_from_input_cert(path:str):
    logger.info(f"open certificate file : {path}")
    file = None
    try:
        cert = cert_handler.read_cert_from_file(path)
        dn = cert_handler.get_subject_dn(cert)
        issuerdn = cert_handler.get_issuer_dn(cert)
        issuercn = cert_handler.get_issuer_cn(cert)
        cn = cert_handler.get_subject_cn(cert)
        keyid = cert_handler.get_subject_key_identifier(cert)
        issuerkeyid = cert_handler.get_authorithy_key_identifier(cert)
        isca = cert_handler.get_is_ca(cert)
        blob = cert_handler.serialize_cert(cert)

        subject_file_id = create_file_id(cert)
        issuer_file_id = create_issuer_file_id(cert)

        file = Cert_Model(subject_file_id=subject_file_id,
                    issuer_file_id=issuer_file_id,
                    cn=cn,
                    dn=dn,
                    isca=isca,
                    blob=blob,
                    issuerdn=issuerdn,
                    issuercn=issuercn,
                    keyid=keyid)
        return file
    except Exception as e:
        logger.error(e, exc_info=True)

    return file

def parse_crl_ocsp_from_cert_model(input_model: Cert_Model) -> tuple[list[CRL_Model],list[OCSP_Model]] :
    crls:list[CRL_Model] = []
    ocsps:list[OCSP_Model] = []

    try:
        cert = cert_handler.read_cert_from_pem_str(input_model.blob)
        crl_urls = cert.get_crls()
        ocsp_urls = cert.get_ocsps()

        for crl_url in crl_urls:
            crl = CRL_Model(issuer_file_id=)

    except Exception as e:
        logger.error(e,exc_info=True)

def handle_upload(path:str) -> list[Cert_Model]:
    
    is_zip_file = zipfile.is_zipfile(path)

    if(is_zip_file):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(param.TEMP)
        os.remove(path)

    elif(cert_handler.check_is_certificate(path)):
        filename = os.path.basename(path)
        shutil.move(path,os.path.join(param.TEMP, filename))
    
    else:
        os.remove(path)
    
    list_file = read_file_input(res=[])

    files: list[Cert_Model] = []
    for file_ in list_file:
        file = parse_file_from_input_cert(file_)

        files.append(file)

        os.remove(file_)

    return files