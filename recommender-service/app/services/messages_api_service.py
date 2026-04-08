from click.utils import R
import requests
import os
from datetime import datetime

from app.schemas import DeviceRecordSchema, DeviceSchema

class MessagesApiService:
    def __init__(self):
        self.base_url = f"http://messages-service:{os.environ.get("MESSAGES_SERVICE_PORT", "5002")}/api"

    def get_messages(self, start: datetime, end: datetime) -> list[DeviceRecordSchema]:
        try:
            url = f"{self.base_url}/dev_messages"
            params = {
                "start": start.isoformat(),
                "end": end.isoformat(),
            }
            response = requests.get(url, params=params)
            response.raise_for_status() 

            data = response.json()
            raw_messages = data.get("messages", [])

            messages = [DeviceRecordSchema(**msg) for msg in raw_messages]

            return messages
        except requests.RequestException as e:
            raise RuntimeError(f"Error retrieving messages from messages-service: {e}")

    def get_devices(self) -> list[DeviceSchema]:
        try:
            url = f"{self.base_url}/devices"
            response = requests.get(url)
            response.raise_for_status() 

            data = response.json()
            raw_devices = data.get("devices", [])

            devices = [DeviceSchema(**msg) for msg in raw_devices]

            return devices
        except requests.RequestException as e:
            raise RuntimeError(f"Error retrieving devices from messages-service: {e}")


