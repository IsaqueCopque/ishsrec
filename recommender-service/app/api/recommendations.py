"""Recommendation API endpoints."""

from flask import Blueprint, request, jsonify

from app.services.rec_service import RecommendationService

service = RecommendationService()

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    """
    GET /api/recommendations?limit=10
    Returns recommendations
    """
    limit = request.args.get("limit", default=10, type=int)
    limit = min(max(limit, 1), 100)
    recommendations = service.generate_recommendations()

    if recommendations is not None:
        recommendations = recommendations[:limit]
    return jsonify({"recommendations": recommendations})
