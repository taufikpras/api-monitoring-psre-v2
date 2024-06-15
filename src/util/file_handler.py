import hashlib
import os
import src.util.cert_handler as cert_handler
import zipfile
import shutil
import pathlib
import src.parameters as param
import logging
from cryptography.x509.base import Certificate
from src.model.file import File 

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

def parse_input_cert(path:str):
    retval = {}
    logger.info(f"open certificate file : {path}")
    file = None
    ca = None
    crls = []
    ocsps = []
    try:
        cert = cert_handler.read_cert_from_file(path)
        dn = cert_handler.get_subject_dn(cert)
        cn = cert_handler.get_subject_cn(cert)
        keyid = cert_handler.get_subject_key_identifier(cert)
        issuerkeyid = cert_handler.get_authorithy_key_identifier(cert)
        isca = cert_handler.get_is_ca(cert)
        blob = cert_handler.serialize_cert(cert)

        subject_file_id = create_file_id(cert)
        issuer_file_id = create_issuer_file_id(cert)

        file = File(subject_file_id=subject_file_id,
                    issuer_file_id=issuer_file_id,
                    cn=cn,
                    dn=dn,
                    isca=isca,
                    blob=blob,
                    keyid=keyid)
        # for crl_url in crl_urls:
        #     crl = CRL(issuer_file_id=issuer_file_id, url=crl_url)
        #     crls.append(crl)
        
        # for ocsp_url in ocsp_urls:
        #     ocsp = OCSP(issuer_file_id=issuer_file_id, subject_file_id=subject_file_id,url=ocsp_url)
        #     ocsps.append(ocsp)

        # if isca == False:
        #     ca = CA(cn=issuercn, dn=issuerdn, keyid=issuerkeyid, crls=crls, ocsps=ocsps)
        # if os.path.isfile(getDataPath(data_filename)) == False:
        #     shutil.copyfile(getInputPath(path), getDataPath(data_filename))
        return file
    except Exception as e:
        logger.error(e, exc_info=True)

    return file

def handle_upload(path:str) -> list[File]:
    
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

    files: list[File] = []
    for file_ in list_file:
        file = parse_input_cert(file_)

        files.append(file)

        os.remove(file_)

    return files