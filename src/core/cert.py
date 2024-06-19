from src.db_schema.cert import Cert_Schema as file_schema
from src.db_schema.database import db
from src.model.cert import Cert_Model, to_list_of_object_from_db, to_object_from_db, convert_to_schema
import src.util.file_handler as file_handler
from bson import ObjectId
import logging

logger = logging.getLogger("monitoring_psre")
COLLECTION_NAME = "cert"

def get_all() -> list[Cert_Model]:
    collection = db[COLLECTION_NAME]
    result = to_list_of_object_from_db(collection.find())
    return result

def get_one(id:str):
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"_id":ObjectId(id)}))
    return result

def find_file(input: Cert_Model) -> Cert_Model:
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"dn":input.dn, "keyid":input.keyid}))
    return result

def find_file_from_file_id(file_id:str) -> Cert_Model:
    collection = db[COLLECTION_NAME]
    result = to_object_from_db(collection.find_one({"subject_file_id":file_id}))
    return result

def update(input: Cert_Model):
    collection = db[COLLECTION_NAME]
    db_schema = convert_to_schema(input)
    res = collection.find_one_and_update({"_id":ObjectId(input.id)}, {"$set": dict(db_schema)},return_document=True)
    return to_object_from_db(res)

def insert_one(input:Cert_Model) -> Cert_Model:
    collection = db[COLLECTION_NAME]
    db_schema = convert_to_schema(input)

    existing = find_file(input)
    res = input
    if(existing == None):
        id = collection.insert_one(dict(db_schema)).inserted_id
        res.id = str(id)
    else:
        res = update(existing)
    return res


def insert_from_file(file_path:str) -> list[Cert_Model]:
    files = file_handler.handle_upload(file_path)
    
    for file in files:
        res = insert_one(file)
        file.id = res.id
    return files
