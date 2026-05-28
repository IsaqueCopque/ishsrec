"""REST API blueprints."""

from app.api.device_messages import dev_messages_bp
from app.api.devices import devices_bp

__all__ = ["dev_messages_bp", "devices_bp"]
