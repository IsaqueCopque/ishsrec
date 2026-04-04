from datetime import datetime
from flask import Blueprint, request, jsonify
from app.services import DeviceRecordService

dev_messages_bp = Blueprint("dev_messages", __name__)

service = DeviceRecordService()

@dev_messages_bp.route("/", methods=["GET"])
def get_messages():
    """
    GET /api/messages?deviceId=<id>&limit=<limit>&start=<start>&end=<end>
    List devices messages. Optional device id.
    """
    device_id = request.args.get("deviceId")
    limit = int(request.args.get("limit") or 100)
    start_str = request.args.get("start")
    end_str = request.args.get("end")

    start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S") if start_str else None
    end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S") if end_str else None
    
    messages = service.find_device_records(
        device_id=device_id, 
        limit=limit, 
        start=start, 
        end=end
    )
    return jsonify({"messages": messages})
