from typing import List
from bson import ObjectId
from bson.errors import InvalidId

from app.db import get_device_collection
from app.schemas import DeviceSchema


class DeviceRepository:

    def __init__(self):
        self.collection = get_device_collection()

    def insert(self, device: DeviceSchema) -> str:
        data = device.model_dump(by_alias=True)
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

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

    """Find a single device by its hardware_id, return as dict or None."""
    def find_by_hardware_id(self, hardware_id: str) -> dict | None:
        return self.collection.find_one({"hardware_id": hardware_id})

