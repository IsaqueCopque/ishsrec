"""Flask app factory for messages-service."""

import os
from flask import Flask
from app.api import dev_messages_bp, devices_bp

def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config or {})
    app.config.setdefault("MESSAGES_MONGO_URI", os.environ.get("MESSAGES_MONGO_URI", "mongodb://localhost:27017/messagesdb"))
    app.config.setdefault("RABBITMQ_HOST", os.environ.get("RABBITMQ_HOST", "rabbitmq"))
    app.config.setdefault("RABBITMQ_PORT", int(os.environ.get("RABBITMQ_PORT", "5672")))
    app.config.setdefault("RABBITMQ_USERNAME", os.environ.get("RABBITMQ_USERNAME", "ishsrec"))
    app.config.setdefault("RABBITMQ_PASSWORD", os.environ.get("RABBITMQ_PASSWORD", "ishsrec"))

   
    app.register_blueprint(dev_messages_bp, url_prefix="/api/dev_messages")
    app.register_blueprint(devices_bp, url_prefix="/api/devices")

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
