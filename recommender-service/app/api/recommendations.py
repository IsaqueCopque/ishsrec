"""Recommendation API endpoints."""

from flask import Blueprint, request, jsonify

from app.services.recommendation_service import recommendation_service

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    """
    GET /api/recommendations?residentId=1&limit=10
    Returns recommendations for the given resident (e.g. similar residents by status).
    """
    resident_id = request.args.get("residentId", type=int)
    if resident_id is None:
        return jsonify({"error": "residentId is required"}), 400
    limit = request.args.get("limit", default=10, type=int)
    limit = min(max(limit, 1), 100)
    recommendations = recommendation_service.get_recommendations(resident_id, limit=limit)
    return jsonify({"residentId": resident_id, "recommendations": recommendations})
