from app.repositories import DeviceRepository


class DeviceService:

    def __init__(self):
        self._repo = DeviceRepository()

    def list_devices(self, device_id: str = None) -> list[dict]:
        return self._repo.list_devices(device_id)