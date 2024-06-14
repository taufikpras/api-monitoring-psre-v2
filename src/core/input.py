import src.util.cert_handler as cert
# import src.core.ca_core as ca_core
# import src.core.web_core as web_core
# import src.core.ocsp_core as ocsp_core
# import src.core.cps_core as cps_core
# import src.core.crl_core as crl_core
# from src.model.input import Input, setInput
import logging

logger = logging.getLogger('monitoring_psre')

# def add_new(input:Input):
#    ca_cert_data = cert.parse_input_cert(input.ca_file_name)
#    user_cert_data = cert.parse_input_cert(input.user_file_name)
#    ca_id = ""
   
#    if(ca_cert_data["keyid"] != user_cert_data["issuerkeyid"]):
#       return None
   
#    existing_ca = ca_core.find_ca(ca_cert_data["dn"],ca_cert_data["keyid"])
#    if(existing_ca == None):
#       ca_id = ca_core.insert(ca_cert_data["cn"],ca_cert_data["dn"], ca_cert_data["keyid"])
#    else:
#       ca_id = existing_ca["id"]

#    if(input.web_url != ""):
#       if(web_core.find_url(ca_id,input.web_url) == None):
#          web_core.insert(ca_id,input.web_url)

#    if(input.cps_url != ""):
#        if(cps_core.find_url(ca_id,input.cps_url) == None):
#          cps_core.insert(ca_id,input.cps_url)

#    for crl in user_cert_data["crl"]:
#       if(crl_core.find_url(ca_id, crl) == None):
#          crl_core.insert(ca_id, crl, ca_cert_data["data_filename"])
   
#    for ocsp in user_cert_data["ocsp"]:
#       # logger.info(ca_cert_data["data_filename"])
#       if(ocsp_core.find_url(ca_id, ocsp) == None):
#          ocsp_core.insert(ca_id, ocsp, user_cert_data["data_filename"], ca_cert_data["data_filename"])

#    return ca_id

# def add_all_file():
#    users, cas= cert.create_cert_input_list()
#    ret = {}
#    ret["user"], ret["ca"] = users, cas

#    for user in users.values():
#       if user["issuerkeyid"] in cas:
#          input = setInput(user["filename"], cas[user["issuerkeyid"]]["filename"])

#          add_new(input)

#    return ret

   

   


