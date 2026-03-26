import os
from pymongo import MongoClient
from pymongo.collection import Collection

class MongoConnection:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        
    def get_device_record_collection(self):
        return self.db['device_records']

connection = MongoConnection(os.environ.get("MESSAGES_MONGO_URI"), os.environ.get("MESSAGES_MONGO_DB"))

def get_device_record_collection() -> Collection:
        return connection.db['device_records']