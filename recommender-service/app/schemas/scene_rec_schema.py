from pydantic import BaseModel, Field

class Condition(BaseModel):
    days_hours: dict[str, list[str]]  # day : hours
    sensors: dict[str, list[str]]     # sensors: sensors values

class SceneRecSchema(BaseModel):
    """Scene Recommendation Schema"""

    days_hours: dict[str, list[str]]    # day : hours
    sensors: dict[str, list[str]]       # sensors: sensors values
    actuators : list[str] = Field(...)  # actuators devices
