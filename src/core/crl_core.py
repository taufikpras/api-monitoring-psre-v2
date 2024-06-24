from src.model.crl import CRL, list_serial,setCRL,individual
from src.db_schema.database import db
from bson import ObjectId
import src.util.net_handler as net_handler

COLLECTION_NAME = "crl"

def get_all():
    collection = db[COLLECTION_NAME]
    results = list_serial(collection.find())
    for result in results:
        ca_data = ca_core.get_one(result["ca_id"])
        result["cn"] = ca_data["cn"]
        result["dn"] = ca_data["dn"]
    return results

def get_one(id:str):
    collection = db[COLLECTION_NAME]
    result = individual(collection.find_one({"_id":ObjectId(id)}))
    ca_data = ca_core.get_one(result["ca_id"])
    result["cn"] = ca_data["cn"]
    result["dn"] = ca_data["dn"]

    return result

def insert_one(input:CRL):
    collection = db[COLLECTION_NAME]
    input.url = net_handler.check_url(input.url)
    res = collection.insert_one(dict(input))
    return str(res.inserted_id)

def insert(ca_id:str, crl_url:str, filename:str):
    crl_model = setCRL(ca_id,crl_url,filename)
    return insert_one(crl_model)

def edit_one(id:str, input:CRL):
    collection = db[COLLECTION_NAME]
    input.url = net_handler.check_url(input.url)
    res = collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(input)},return_document=True)
    return individual(res)

def delete_one(id:str):
    collection = db[COLLECTION_NAME]
    return str(collection.find_one_and_delete({"_id": ObjectId(id)}))

def find_url(ca_id:str, url:str):
    collection = db[COLLECTION_NAME]
    url = net_handler.check_url(url)
    result = individual(collection.find_one({"ca_id":ca_id, "url":url}))
    return result

def find_ca_id(ca_id:str):
    collection = db[COLLECTION_NAME]
    results = list_serial(collection.find({"ca_id":ca_id}))
    return results