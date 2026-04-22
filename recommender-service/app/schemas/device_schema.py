from pydantic import BaseModel, ConfigDict, Field

class DeviceSchema(BaseModel):
    """Device document stored in `devices` collection."""

    hardware_id: str = Field(..., alias="externalId")
    name: str
    type: str
    model: str
    manufacturer: str
    firmware_version :str

    model_config = ConfigDict(populate_by_name=True)
