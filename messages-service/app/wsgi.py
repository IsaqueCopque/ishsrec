"""WSGI entry point: creates app and starts RabbitMQ consumers."""

import logging
from app import create_app
from app.messaging import RabbitConsumer

logging.basicConfig(level=logging.INFO)
app = create_app()

consumer = RabbitConsumer()
consumer.start_consumer()