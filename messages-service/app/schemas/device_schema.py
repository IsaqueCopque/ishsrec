from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceSchema(BaseModel):
    """Device document stored in `devices` collection."""

    external_id: str = Field(..., alias="externalId")
    name: str
    device_type: str = Field(..., alias="type")
    model: str
    manufacturer: str

    model_config = ConfigDict(populate_by_name=True)
