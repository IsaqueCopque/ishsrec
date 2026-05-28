"""Flask app factory for recommender-service."""

import os
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config or {})
    app.config.setdefault("RABBITMQ_HOST", os.environ.get("RABBITMQ_HOST", "localhost"))
    app.config.setdefault("RABBITMQ_PORT", int(os.environ.get("RABBITMQ_PORT", "5672")))
    app.config.setdefault("RABBITMQ_USERNAME", os.environ.get("RABBITMQ_USERNAME", "ishsrec"))
    app.config.setdefault("RABBITMQ_PASSWORD", os.environ.get("RABBITMQ_PASSWORD", "ishsrec"))

    from app.api import recommendations_bp
    app.register_blueprint(recommendations_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
