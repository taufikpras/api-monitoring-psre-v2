from pymongo.mongo_client import MongoClient
import src.parameters as param

MONGO_URL = f"mongodb://{param.MONGO_USER}:{param.MONGO_PASS}@{param.MONGO_HOST}:{param.MONGO_PORT}/"

client = MongoClient(MONGO_URL)

db = client.monitoring
