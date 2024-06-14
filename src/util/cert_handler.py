import os
from cryptography import x509
from cryptography.x509.oid import ExtensionOID
from cryptography.hazmat.backends import default_backend
from cryptography.x509.base import Certificate
from cryptography.x509.oid import NameOID
import logging
import hashlib
import shutil

from cryptography.x509 import ocsp
from cryptography.x509.ocsp import OCSPCertStatus
from cryptography.hazmat.primitives.hashes import SHA256, SHA1
from cryptography.hazmat.primitives import serialization

from datetime import datetime, timedelta, timezone

import requests

logger = logging.getLogger('monitoring_psre')

from src.exception.cert_exception import EncodingException
from src.parameters import INPUT_PATH, DATA_PATH

def readFileInput(path, res:list):
    # res = []
    for path_ in os.listdir(path):
        # check if current path is a file
        if os.path.isfile(os.path.join(path, path_)):
            res.append(os.path.join(path, path_))
        else:
            readFileInput(os.path.join(path, path_), res)
    return res

def checkIsCertFile(path):
    returnval = False
    try:
        with open(path, 'rb') as cert_file:  # try open file in text mode
            certdata = cert_file.read()
        returnval = x509.load_pem_x509_certificate(certdata, default_backend())
        returnval = True
    except:  # if fail then file is non-text (binary)
        print("Not in PEM")
    
    try:
        with open(path, 'rb') as cert_file:    
            certdata = cert_file.read()
        returnval = x509.load_der_x509_certificate(certdata, default_backend())
        returnval = True
    except:
        print("Not in DER")
        
    return returnval

def readCert(path) -> Certificate | None:
    returnval = None
    
    try:
        with open(path, 'rb') as cert_file:  # try open file in text mode
            certdata = cert_file.read()
        returnval = x509.load_pem_x509_certificate(certdata, default_backend())
        returnval = True
    except:  # if fail then file is non-text (binary)
        print("Not in PEM")
    
    try:
        with open(path, 'rb') as cert_file:    
            certdata = cert_file.read()
        returnval = x509.load_der_x509_certificate(certdata, default_backend())
        returnval = True
    except:
        print("Not in DER")
        
    if returnval == None:
        raise EncodingException("Encoding Format Unknown")
        
    return returnval

def getIssuerCN(cert: Certificate):
    cn = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    return cn

def getSubjectCN(cert: Certificate):
    cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    return cn

def getSubjectDN(cert: Certificate):
    dn = cert.subject.rfc4514_string()
    return dn

def getIssuertDN(cert: Certificate):
    dn = cert.issuer.rfc4514_string()
    return dn

def getAuthorityKeyIdentifier(cert: Certificate):
    # retur self.userWrapper.extensions.get_extension_for_oid(x509.ExtensionOID.AUTHORITY_KEY_IDENTIFIER).value.key_identifier.hex()
    authorityKeyId = cert.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier).value.key_identifier.hex()
    return authorityKeyId
    
def getSubjectKeyIdentifier(cert: Certificate):
    subjectKeyID = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_KEY_IDENTIFIER).value.digest.hex()
    return subjectKeyID

def getIsCA(cert: Certificate):
    val = cert.extensions.get_extension_for_oid(x509.ExtensionOID.BASIC_CONSTRAINTS).value.ca
    return val

def getCRLs(cert: Certificate) -> list[str]:
    urls = []
    try:
        crldps = cert.extensions.get_extension_for_oid(x509.ExtensionOID.CRL_DISTRIBUTION_POINTS).value
        for crldp in crldps:
            full_name = crldp.full_name
            for url in full_name:
                urls.append(url.value)
    except x509.ExtensionNotFound:
        logger.warning("CRL DP Extension not found")
    
    return urls

def getOCSPs(cert: Certificate) -> list[str]:
    ocsp = []
    try:
        if (len(cert.extensions.get_extension_for_oid(
                x509.ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value) > 0):
            # ocspList = self.x509wrapper.extensions.get_extension_for_oid(x509.ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value[1].access_location.value
            ocspList = cert.extensions.get_extension_for_oid(
                x509.ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value
            for i in ocspList:
                if (i.access_method.dotted_string == "1.3.6.1.5.5.7.48.1"):
                    ocsp.append(i.access_location.value)
    except x509.ExtensionNotFound:
        return None
    
    return ocsp



