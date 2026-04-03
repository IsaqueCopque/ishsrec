from typing import List
from bson import ObjectId
from bson.errors import InvalidId

from app.db import get_device_collection


class DeviceRepository:

    def __init__(self):
        self.collection = get_device_collection()

    def exists_by_id(self, device_id: str) -> bool:
        try:
            oid = ObjectId(device_id)
        except (InvalidId, TypeError):
            return False
        return self.collection.count_documents({"_id": oid}, limit=1) > 0

    def list_devices(self, device_id: str = None) -> List[dict]:
        query ={}
        if device_id is not None:
            query["_id"] = ObjectId(device_id)
        cursor = self.collection.find(query).sort("name", 1)
        return list(cursor)
