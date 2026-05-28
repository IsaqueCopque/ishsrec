from datetime import datetime
from typing import List, Optional

from app.db import get_device_record_collection
from app.schemas import DeviceRecordSchema


def _normalize_record(doc: dict) -> dict:
    out = dict(doc)
    if "_id" in out:
        out["_id"] = str(out["_id"])
    return out


class DeviceRecordRepository:

    def __init__(self):
        self.collection = get_device_record_collection()

    def insert(self, record: DeviceRecordSchema) -> str:
        data = record.model_dump(by_alias=True)
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def find_all(self, limit: int = 100) -> List[dict]:
        cursor = (
            self.collection.find().sort("timestamp", -1).limit(limit)
        )
        return [_normalize_record(d) for d in cursor]

    def find_by_device(
        self,
        device_id: str,
        limit: int = 100,
    ) -> List[dict]:
        cursor = (
            self.collection
            .find({"deviceId": device_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return [_normalize_record(d) for d in cursor]

    def find_by_timerange(
        self,
        start: datetime,
        end: datetime,
        device_id: Optional[str] = None
    ) -> List[dict]:

        query = {
            "timestamp": {
                "$gte": start,
                "$lte": end
            }
        }

        if device_id is not None:
                query["deviceId"] = device_id

        cursor = self.collection.find(query).sort("timestamp", 1)
        return [_normalize_record(d) for d in cursor]

    def delete_by_device(self, device_id: str) -> int:
        result = self.collection.delete_many({"deviceId": device_id})
        return result.deleted_count

    def delete_by_timerange(self, start: datetime, end: datetime) -> int:
        result = self.collection.delete_many({"timestamp": { "$gte": start, "$lte": end}})
        return result.deleted_count