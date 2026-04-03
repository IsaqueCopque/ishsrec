from flask import Blueprint, jsonify, request

from app.services import DeviceService

devices_bp = Blueprint("devices", __name__)
_service = DeviceService()


@devices_bp.route("/devices", methods=["GET"])
def list_devices():
    """
    GET /api/devices
    List registered devices for the resident's home (no message history).
    """
    devices = _service.list_devices()
    return jsonify({"devices": devices})
