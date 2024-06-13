from src.model.ca import CA, setCA, to_object, list_object
from src.model.database import db
# import src.core.web_core as web_core
# import src.core.cps_core as cps_core
# import src.core.crl_core as crl_core
# import src.core.ocsp_core as ocsp_core
from bson import ObjectId

COLLECTION_NAME = "ca"

def get_all():
    collection = db[COLLECTION_NAME]
    result = list_object(collection.find())
    return result

def get_one(id:str):
    collection = db[COLLECTION_NAME]
    result = to_object(collection.find_one({"_id":ObjectId(id)}))
    return result

def insert_one(input:CA):
    collection = db[COLLECTION_NAME]
    res = collection.insert_one(dict(input))
    return str(res.inserted_id)

def insert(cn:str, dn:str, keyid:str):
    model_ = setCA(cn,dn,keyid)
    return insert_one(model_)

def edit_one(id:str, input:CA):
    collection = db[COLLECTION_NAME]
    res = collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(input)},return_document=True)
    return to_object(res)

def delete_one(id:str):
    collection = db[COLLECTION_NAME]
    return str(collection.find_one_and_delete({"_id": ObjectId(id)}))

def find_ca(dn:str, keyid:str):
    collection = db[COLLECTION_NAME]
    result = to_object(collection.find_one({"dn":dn, "keyid":keyid}))
    return result

# def get_all_ca_and_component():
#     cas = get_all()
    
#     for ca in cas:
#         ca_id = ca["id"]
#         ca["web"] = web_core.find_ca_id(ca_id)
#         ca["ocsp"] = ocsp_core.find_ca_id(ca_id)
#         ca["crl"] = crl_core.find_ca_id(ca_id)
#         ca["cps"] = cps_core.find_ca_id(ca_id)
    
#     return cas
