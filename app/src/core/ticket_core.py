from src.db_schema.ticket_schema import to_object_from_db, to_list_of_object_from_db, Tickets_Schema
from src.db_schema.database import db
from bson import ObjectId
from datetime import datetime, timedelta

import logging
import src.parameters as param
logger = logging.getLogger(param.LOGGER_NAME)

COLLECTION_NAME = "tickets"
MIN_OCCURANCE = 5

def get_all_active():
    collection = db[COLLECTION_NAME]
    result = to_list_of_object_from_db(collection.find({"resolve":False}))
    return result

def insert_one(input:TicketsInput):
    collection = db[COLLECTION_NAME]
    exist = find_active_tickets(input.ca_id, input.obj_id)
    
    if(exist == None):
        input = set_ticket_from_input(input)
        res = collection.insert_one(dict(input))
        res = str(res.inserted_id)
    else:
        res = exist["id"]
    return get_one(res)

def delete_one(id:str):
    collection = db[COLLECTION_NAME]
    return str(collection.find_one_and_delete({"_id": ObjectId(id)}))

def update(id:str, input:Tickets):
    collection = db[COLLECTION_NAME]
    res = collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(input)},return_document=True)
    return individual(res)

def find_active_tickets(ca_id:str, obj_id:str):
    collection = db[COLLECTION_NAME]
    uid = create_uid(ca_id, obj_id)
    result = individual(collection.find_one({"uid":uid, "resolve":False}))
    return result

def set_resolve(ca_id:str, obj_id:str):
    collection = db[COLLECTION_NAME]
    uid = create_uid(ca_id, obj_id)
    result = collection.find_one({"uid":uid, "resolve":False})

    if(result != None):
        result["resolve"] = True
        result["last_notif"] = None
        result["end"] = datetime.now()

        if(result["occurance"] < MIN_OCCURANCE):
            res = delete_one(result["_id"])
        else:
            res = collection.find_one_and_update({"_id":ObjectId(result["_id"])}, {"$set": result},return_document=True)
            res = individual(res)
    else:
        res = None
    return res

def log_ticket(input:dict, verification:dict, message):
    active = find_active_tickets(input["ca_id"],input["id"])
    ret = None
    if(verification['overall'] == 0):
        if(active == None):
            logger.info(f'Tickets created : {input["cn"]}')
            ticket = TicketsInput(ca_id=input["ca_id"],
                        cn=input["cn"],
                        obj_id=input["id"],
                        message=f'{input["cn"]} - {message} - {input["url"]}',
                        url=input["url"])
            ret = insert_one(ticket)
        else:
            logger.info(f'Update Occurance : {input["cn"]}')
            active["occurance"] = active["occurance"] + 1
            active_ = to_object(active)
            ret = update(id=active["id"], input=active_)
    else:
        if active != None:
            logger.info(f'Tickets resolved : {input["cn"]}')
            ret = set_resolve(input["ca_id"],input["id"])
    return ret

def get_ticket_for_realtime_notif():
    collection = db[COLLECTION_NAME]

    time_ = datetime.now() - timedelta(hours=2)
    new_notif = {"$and":[{"last_notif":None},{"occurance":{"$gte":MIN_OCCURANCE}}]}
    old_notif = {"$and":[{'last_notif': {"$lte": time_}},{"resolve":False}]}
    params = {"$or":[old_notif, new_notif]}

    result = collection.find(params)
    return list_serial(result)

def get_ticket_for_reguler_report():
    collection = db[COLLECTION_NAME]

    time_ = datetime.now() - timedelta(days=7)
    params = {'start': {"$gte": time_}}

    result = collection.find(params)
    return list_serial(result)

def update_last_notif(id):
    collection = db[COLLECTION_NAME]
    result = collection.find_one({"_id":ObjectId(id)})
    result["last_notif"] = datetime.now()
    res = collection.find_one_and_update({"_id":ObjectId(result["_id"])}, {"$set": result},return_document=True)
    return individual(res)






