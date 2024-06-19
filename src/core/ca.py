from src.model.cert import Cert_Model
from src.model.ca import CA_Model, convert_to_schema, to_object_from_db, to_list_of_object_from_db
from src.db_schema.database import db
from bson import ObjectId

COLLECTION_NAME = "ca"

def get_all():
    collection = db[COLLECTION_NAME]
    result = to_list_of_object_from_db(collection.find())
    return result

def get_one(id:str):
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"_id":ObjectId(id)}))
    return result

def insert_one(input_file:CA_Model):
    collection = db[COLLECTION_NAME]
    schema = convert_to_schema(input_file)
    res = collection.insert_one(dict(schema))
    input_file.id = res.inserted_id
    return input_file

def edit_one(input_file:CA_Model):
    collection = db[COLLECTION_NAME]
    schema = convert_to_schema(input_file)
    res = collection.find_one_and_update({"_id":ObjectId(input_file.id)}, {"$set": dict(schema)},return_document=True)
    return to_object_from_db(res)

def delete_one(id:str):
    collection = db[COLLECTION_NAME]
    return str(collection.find_one_and_delete({"_id": ObjectId(id)}))

def find_ca_by_dn_keyid(input_file:CA_Model):
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"dn":input_file.dn, "keyid":input_file.keyid}))
    return result

def insert_from_file(input_file: CA_Model):
    collection = db[COLLECTION_NAME]
    


# def get_all_ca_and_component():
#     cas = get_all()
    
#     for ca in cas:
#         ca_id = ca["id"]
#         ca["web"] = web_core.find_ca_id(ca_id)
#         ca["ocsp"] = ocsp_core.find_ca_id(ca_id)
#         ca["crl"] = crl_core.find_ca_id(ca_id)
#         ca["cps"] = cps_core.find_ca_id(ca_id)
    
#     return cas
