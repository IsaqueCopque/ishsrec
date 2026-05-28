from datetime import datetime
import logging

from typing import Any,Optional

from pydantic import ValidationError

from app.repositories import DeviceRecordRepository, DeviceRepository
from app.schemas import DeviceRecordSchema, DeviceSchema

logger = logging.getLogger(__name__)


class DeviceRecordService:

    def __init__(self):
        self._repo = DeviceRecordRepository()
        self._devices = DeviceRepository()

    def create_device_record(self, payload: dict[str, Any]) -> Optional[str]:
        try:
            dev_record = DeviceRecordSchema.model_validate(payload)
        except ValidationError as e:
            logger.error(
                "Invalid device record",
                extra={"payload": payload, "errors": e.errors()}
            )
            return None

        try:
            device_id = self._handle_device_creation(dev_record)
            dev_record.device_id = device_id
            logger.info("New device registered", extra={"device_id": dev_record.device_id})
        except ValidationError as e:
            logger.error(
                "Invalid device record to create device",
                extra={"payload": payload, "errors": e.errors()}
            )
            return None

        record_id = self._repo.insert(dev_record)
        logger.info("Device record created", extra={"record_id": record_id, "device_id": dev_record.device_id})
        return record_id

    def _handle_device_creation(self, dev_record: DeviceRecordSchema) -> str:
        """Creates a new device if registering or returns the existing device_id"""
        
        if dev_record.type != 'register':
            if not dev_record.device_id:
                raise ValidationError(
                    [{"loc": ("device_id",), "msg": "device_id is required for non-register records", "type": "value_error"}],
                    model=DeviceSchema
                )
            return dev_record.device_id

        hardware_id = dev_record.device_hardware_id
        if not hardware_id:
            raise ValidationError(
                [{"loc": ("device_hardware_id",), "msg": "device_hardware_id is required for device registration", "type": "value_error"}],
                model=DeviceSchema
            )

        device = self._devices.find_by_hardware_id(hardware_id=hardware_id)
        if device:
            return str(device['_id'])

        device_dict = {
            'hardware_id': hardware_id,
            'name': dev_record.device_name,
            'type': dev_record.device_type,
            'model': dev_record.device_model,
            'manufacturer': dev_record.device_manufacturer,
            'firmware_version': dev_record.device_firmware_version
        }

        device_obj = DeviceSchema.model_validate(device_dict)
        device_id = self._devices.insert(device_obj)
        return device_id


    def find_device_records(
        self,
        device_id: str | None,
        limit: int,
        start: datetime | None,
        end: datetime | None
    ) -> list[dict]:

        has_timerange = start is not None and end is not None

        if device_id:
            if has_timerange:
                return self._repo.find_by_device(
                    device_id=device_id,
                    start=start,
                    end=end
                )
            return self._repo.find_by_device(
                device_id=device_id,
                limit=limit
            )

        if has_timerange:
            return self._repo.find_by_timerange(
                start=start,
                end=end
            )

        return self._repo.find_all(limit=limit)