import os
import src.util.cert_handler as cert_handler
import zipfile
import shutil
import pathlib
import src.parameters as param
import logging

logger = logging.getLogger('monitoring_psre')



def read_file_input(path=cert_handler.INPUT_PATH, res:list=[]):
    # res = []
    for path_ in os.listdir(path):
        # check if current path is a file
        if os.path.isfile(os.path.join(path, path_)):
            # print(os.path.join(path, path_))
            res.append(os.path.join(path, path_))
        else:
            read_file_input(os.path.join(path,path_), res)
    return res

def handle_upload(path:str):
    
    is_zip_file = zipfile.is_zipfile(path)

    if(is_zip_file):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(param.INPUT_PATH)
        os.remove(path)

    elif(cert_handler.checkIsCertFile(path)):
        filename = os.path.basename(path)
        shutil.move(path,os.path.join(param.INPUT_PATH, filename))
    
    else:
        os.remove(path)
    
    return read_file_input(res=[])


def getInputPath(filename:str):
    if(filename.startswith(param.INPUT_PATH)):
        return filename
    else:
        return os.path.join(param.INPUT_PATH,filename)

def getDataPath(filename:str):
    if(filename.startswith(param.DATA_PATH)):
        return filename
    else:
        return os.path.join(param.DATA_PATH,filename)
    
    
# def createFileName(cert: Certificate):
#     string_input = getSubjectDN(cert)+"-"+str(getSubjectKeyIdentifier(cert))
#     filename = hashlib.sha1(string_input.encode()).hexdigest()
#     return filename

def parse_input_cert(path:str):
    retval = {}
    logger.info(path)
    try:
        cert = readCert(getInputPath(path))
        retval["dn"] = getSubjectDN(cert)
        retval["cn"] = getSubjectCN(cert)
        retval["issuerdn"] = getIssuertDN(cert)
        retval["issuercn"] = getIssuerCN(cert)
        retval["issuerkeyid"] = getAuthorityKeyIdentifier(cert)
        retval["keyid"] = getSubjectKeyIdentifier(cert)
        retval["crl"] = getCRLs(cert)
        retval["ocsp"] = getOCSPs(cert)

        data_filename = createFileName(cert)
        if os.path.isfile(getDataPath(data_filename)) == False:
            shutil.copyfile(getInputPath(path), getDataPath(data_filename))
        
        retval["data_filename"] = data_filename
    except Exception as e:
        logger.error(e, exc_info=True)

    return retval

def create_cert_input_list():
    path_list = readFileInput(INPUT_PATH, [])
    logger.debug(path_list)
    user_cert_dict = {}
    ca_cert_dict = {}
    for path in path_list:
        logger.debug(path)
        cert = readCert(getInputPath(path))
        cert_data = {}
        cert_data["filename"] = path
        cert_data["issuerkeyid"] = getAuthorityKeyIdentifier(cert)

        if(getIsCA(cert) == False):
            user_cert_dict[getSubjectKeyIdentifier(cert)] = cert_data
        else:
            ca_cert_dict[getSubjectKeyIdentifier(cert)] = cert_data
    
    return user_cert_dict, ca_cert_dict