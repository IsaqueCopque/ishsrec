from flask import Blueprint, request, jsonify
from app.services import DeviceRecordService

dev_messages_bp = Blueprint("dev_messages", __name__)

service = DeviceRecordService()

@dev_messages_bp.route("/messages", methods=["GET"])
def get_messages():
    """
    GET /api/messages?deviceId=<id>&limit=<limit>
    List devices messages. Optional device id.
    """
    device_id = request.args.get("deviceId")
    limit = int(request.args.get("limit") or 100)
    messages= service.find_device_records(device_id=device_id, limit=limit)
    return jsonify(messages)