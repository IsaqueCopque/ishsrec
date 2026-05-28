from typing import Union

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class DeviceRecordSchema(BaseModel):
    """
    State history for a device. `deviceId` is the MongoDB ObjectId string
    of the document in the `devices` collection.
    """

    device_id: str = Field(..., alias="deviceId")
    timestamp: datetime = Field(...)
    action: str = Field(...)
    value: Union[bool, float]

    model_config = ConfigDict(populate_by_name=True)
