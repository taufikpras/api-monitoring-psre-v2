from pymongo.mongo_client import MongoClient

MONGO_URL = "mongodb://root:1234qweR@mongo:27017/"

client = MongoClient(MONGO_URL)

db = client.monitoring
