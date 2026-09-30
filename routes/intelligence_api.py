from functools import wraps

from flask import Blueprint, jsonify, session

from services.inventory_intelligence import (
    get_inventory_alerts,
    get_intelligence_summary,
    get_inventory_intelligence,
    get_product_intelligence,
)


intelligence_api_bp = Blueprint(
    "intelligence_api",
    __name__,
    url_prefix="/api/intelligence"
)


def business_or_admin_required(view_function):
    """Allow only logged-in Business or Admin users."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "status": "error",
                "message": "Authentication required"
            }), 401

        if session.get("role") not in ("Business", "Admin"):
            return jsonify({
                "status": "error",
                "message": "Access denied"
            }), 403

        return view_function(*args, **kwargs)

    return wrapped_view


@intelligence_api_bp.route("", methods=["GET"])
@business_or_admin_required
def get_intelligence():

    data = get_inventory_intelligence()

    return jsonify({
        "status": "success",
        "count": len(data),
        "intelligence": data
    })


@intelligence_api_bp.route(
    "/product/<int:product_id>",
    methods=["GET"]
)
@business_or_admin_required
def product_intelligence(product_id):

    data = get_product_intelligence(product_id)

    if data is None:
        return jsonify({
            "status": "error",
            "message": "Product inventory not found"
        }), 404

    return jsonify({
        "status": "success",
        "product_id": product_id,
        "count": len(data),
        "intelligence": data
    })


@intelligence_api_bp.route(
    "/alerts",
    methods=["GET"]
)
@business_or_admin_required
def intelligence_alerts():

    alerts = get_inventory_alerts()

    return jsonify({
        "status": "success",
        "count": len(alerts),
        "alerts": alerts
    })


@intelligence_api_bp.route(
    "/summary",
    methods=["GET"]
)
@business_or_admin_required
def intelligence_summary():

    summary = get_intelligence_summary()

    return jsonify({
        "status": "success",
        "summary": summary
    })