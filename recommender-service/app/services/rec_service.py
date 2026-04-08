from datetime import datetime, timedelta
from app.services import MessagesApiService, RecModel
import logging

logger = logging.getLogger(__name__)

_messages_service = MessagesApiService()
model = RecModel()

class RecommendationService:

    def __init__(self):
        pass

    def generate_recommendations(self) -> list[dict]:
        today = datetime.now()
        two_weeks_ago = today - timedelta(weeks=2)
        device_records = _messages_service.get_messages(start=two_weeks_ago, end=today)
        devices = _messages_service.get_devices()

        if len(device_records) == 0 or len(devices) == 0:
            logger.warning("No data availabel to the recommender model")
            return []

        model.update_data(device_records, devices)
        model.fit_data()

        recommendations = model.recommend()
        
        return recommendations
