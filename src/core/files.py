from src.db_schema.file import File_Schema as file_schema
from src.db_schema.database import db
from src.model.file import File as file_model
import src.model.file as file_model_func
import src.util.file_handler as file_handler
from bson import ObjectId
import logging

logger = logging.getLogger("monitoring_psre")
COLLECTION_NAME = "file"

def get_all() -> list[file_model]:
    collection = db[COLLECTION_NAME]
    result = file_model_func.to_list_of_object_from_db(collection.find())
    return result

def get_one(id:str):
    collection = db[COLLECTION_NAME]
    result = file_model_func.to_object_from_db(collection.find_one({"_id":ObjectId(id)}))
    return result

def find_file(input: file_model) -> file_model:
    collection = db[COLLECTION_NAME]
    result = file_model_func.to_object_from_db(collection.find_one({"dn":input.dn, "keyid":input.keyid}))
    return result

def update(input: file_model):
    collection = db[COLLECTION_NAME]
    db_schema = file_model_func.convert_to_schema(input)
    res = collection.find_one_and_update({"_id":ObjectId(input.id)}, {"$set": dict(db_schema)},return_document=True)
    return file_model_func.to_object_from_db(res)

def insert_one(input:file_model) -> file_model:
    collection = db[COLLECTION_NAME]
    db_schema = file_model_func.convert_to_schema(input)

    existing = find_file(input)
    res = input
    if(existing == None):
        id = collection.insert_one(dict(db_schema)).inserted_id
        res.id = str(id)
    else:
        res = update(existing)
    return res


def insert_from_file(file_path:str) -> list[file_model]:
    files = file_handler.handle_upload(file_path)
    
    for file in files:
        res = insert_one(file)
        file.id = res.id
    return files



# def insert(cn:str, dn:str, keyid:str):
#     model_ = setCA(cn,dn,keyid)
#     return insert_one(model_)

# def edit_one(id:str, input:CA):
#     collection = db[COLLECTION_NAME]
#     res = collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(input)},return_document=True)
#     return to_object(res)

# def delete_one(id:str):
#     collection = db[COLLECTION_NAME]
#     return str(collection.find_one_and_delete({"_id": ObjectId(id)}))

# def find_ca(dn:str, keyid:str):
#     collection = db[COLLECTION_NAME]
#     result = to_object(collection.find_one({"dn":dn, "keyid":keyid}))
#     return result