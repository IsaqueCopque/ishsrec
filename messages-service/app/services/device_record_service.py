import logging

from typing import Any

from pydantic import ValidationError

from app.repositories import DeviceRecordRepository
from app.schemas import DeviceRecordSchema

logger = logging.getLogger(__name__)

class DeviceRecordService:

    def __init__(self):
        self._repo = DeviceRecordRepository()

    def create_device_record(self, payload: dict[str,Any]):
        try:
            dev_record = DeviceRecordSchema.model_validate(payload)
            self._repo.insert(dev_record)
        except ValidationError as e:
            logger.error("Invalid device record", extra={"payload": payload, "errors": e.errors()})

    def find_device_records(self, device_id: str, limit: int ) -> list[dict]:
        messages = []
        if not device_id:
            messages = self._repo.find_all(limit=limit)
        else:
            messages = self._repo.find_by_device(device_id=device_id, limit=limit)
        return messages