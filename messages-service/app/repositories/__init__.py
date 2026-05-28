"""MongoDB repositories."""

from app.repositories.device_record_repository import DeviceRecordRepository
from app.repositories.device_repository import DeviceRepository

__all__ = ["DeviceRecordRepository", "DeviceRepository"]
