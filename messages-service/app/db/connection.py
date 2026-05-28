import os
from pymongo import MongoClient
from pymongo.collection import Collection

_MONGO_URI = os.environ.get("MESSAGES_MONGO_URI", "mongodb://localhost:27017/messagesdb")
_MONGO_DB = os.environ.get("MESSAGES_MONGO_DB", "messagesdb")


class MongoConnection:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_device_record_collection(self):
        return self.db["device_records"]

    def get_device_collection(self):
        return self.db["devices"]


connection = MongoConnection(_MONGO_URI, _MONGO_DB)


def get_device_record_collection() -> Collection:
    return connection.db["device_records"]

def get_device_collection() -> Collection:
    return connection.db["devices"]