from typing import Union

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class DeviceRecordSchema(BaseModel):
    """
    Registers device messages. 
    New devices connecting messages have "type":"register".
    `deviceId` is the MongoDB ObjectId string of the document in the `devices` collection.
    """

    device_id: str = Field(alias="deviceId") #id in collection
    timestamp: datetime = Field(...)
    action: str = Field(...)
    value: Union[bool, float]
    
    #Registering message used fields
    type : str
    device_hardware_id: str
    device_type : str
    device_model : str
    device_name : str
    device_firmware_version : str
    device_manufacturer : str

    model_config = ConfigDict(populate_by_name=True)
