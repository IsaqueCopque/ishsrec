import logging

from typing import Any

from pydantic import ValidationError

from app.repositories import DeviceRecordRepository, DeviceRepository
from app.schemas import DeviceRecordSchema

logger = logging.getLogger(__name__)


class DeviceRecordService:

    def __init__(self):
        self._repo = DeviceRecordRepository()
        self._devices = DeviceRepository()

    def create_device_record(self, payload: dict[str, Any]):
        try:
            dev_record = DeviceRecordSchema.model_validate(payload)
        except ValidationError as e:
            logger.error("Invalid device record", extra={"payload": payload, "errors": e.errors()})
            return
        if not self._devices.exists_by_id(dev_record.device_id):
            logger.error(
                "device record references unknown device id",
                extra={"deviceId": dev_record.device_id},
            )
            return
        self._repo.insert(dev_record)

    def find_device_records(self, device_id: str, limit: int ) -> list[dict]:
        messages = []
        if not device_id:
            messages = self._repo.find_all(limit=limit)
        else:
            messages = self._repo.find_by_device(device_id=device_id, limit=limit)
        return messages