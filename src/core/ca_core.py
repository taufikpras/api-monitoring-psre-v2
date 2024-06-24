from src.db_schema.file_repo_schema import File_Repo_Schema
from src.db_schema.ca_schema import CA_Schema, to_object_from_db, to_list_of_object_from_db
from src.db_schema.database import db
from src.util import file_handler
from bson import ObjectId
import logging

COLLECTION_NAME = "ca"

logger = logging.getLogger("monitoring_psre")

def get_all() -> list[CA_Schema]:
    collection = db[COLLECTION_NAME]
    result = to_list_of_object_from_db(collection.find())
    return result

def get_one(id:str) -> CA_Schema:
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"_id":ObjectId(id)}))
    return result

def insert_one(input_:CA_Schema) -> CA_Schema:
    collection = db[COLLECTION_NAME]
    # schema = convert_to_schema(input_)
    existing = find_ca_by_dn_keyid(input_)
    res = None
    if(existing == None) :
        res = collection.insert_one(dict(input_))
        # input_._id = res.inserted_id
    else :
        existing = edit_one(existing)
        input_ = existing
    return input_

def edit_one(input_:CA_Schema) -> CA_Schema:
    collection = db[COLLECTION_NAME]
    # schema = convert_to_schema(input_)
    res = collection.find_one_and_update({"dn":input_.dn, "keyid":input_.keyid}, {"$set": dict(input_)},return_document=True)
    return to_object_from_db(res)

def delete_one(id:str):
    collection = db[COLLECTION_NAME]
    return str(collection.find_one_and_delete({"_id": ObjectId(id)}))

def find_ca_by_dn_keyid(input_:CA_Schema):
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"dn":input_.dn, "keyid":input_.keyid}))
    return result

def insert_from_cert(input_file: File_Repo_Schema):
    ca = file_handler.parse_ca_from_file(input_file)

    if ca is not None:
        ca = insert_one(ca)
    
    return ca
    
    


# def get_all_ca_and_component():
#     cas = get_all()
    
#     for ca in cas:
#         ca_id = ca["id"]
#         ca["web"] = web_core.find_ca_id(ca_id)
#         ca["ocsp"] = ocsp_core.find_ca_id(ca_id)
#         ca["crl"] = crl_core.find_ca_id(ca_id)
#         ca["cps"] = cps_core.find_ca_id(ca_id)
    
#     return cas
