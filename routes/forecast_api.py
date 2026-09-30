from functools import wraps

from flask import Blueprint, jsonify, request, session

from database import get_connection
from services.forecast_service import (
    FORECAST_DAYS,
    generate_all_forecasts,
    generate_product_forecast,
)


forecast_api_bp = Blueprint(
    "forecast_api",
    __name__,
    url_prefix="/api/forecast"
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


@forecast_api_bp.route("", methods=["GET"])
@business_or_admin_required
def get_forecasts():
    """Return stored forecasts."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                f.forecast_id,
                f.product_id,
                p.sku,
                p.product_name,
                p.category,
                f.predicted_demand,
                f.forecast_date
            FROM forecast f
            INNER JOIN products p
                ON f.product_id = p.product_id
            ORDER BY f.forecast_date ASC, f.product_id ASC
        """)

        forecasts = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(forecasts),
            "forecasts": forecasts
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve forecasts",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@forecast_api_bp.route("/<int:product_id>", methods=["GET"])
@business_or_admin_required
def get_product_forecast(product_id):
    """Return stored forecasts for one product."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                f.forecast_id,
                f.product_id,
                p.sku,
                p.product_name,
                p.category,
                f.predicted_demand,
                f.forecast_date
            FROM forecast f
            INNER JOIN products p
                ON f.product_id = p.product_id
            WHERE f.product_id = %s
            ORDER BY f.forecast_date ASC
        """, (product_id,))

        forecasts = cursor.fetchall()

        if not forecasts:
            return jsonify({
                "status": "error",
                "message": "No forecast found for this product"
            }), 404

        return jsonify({
            "status": "success",
            "product_id": product_id,
            "count": len(forecasts),
            "forecasts": forecasts
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve product forecast",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@forecast_api_bp.route(
    "/<int:product_id>/generate",
    methods=["POST"]
)
@business_or_admin_required
def generate_forecast(product_id):
    """Generate a new forecast for one product."""

    data = request.get_json(silent=True) or {}

    forecast_days = data.get(
        "forecast_days",
        FORECAST_DAYS
    )

    try:
        forecast_days = int(forecast_days)
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "forecast_days must be an integer"
        }), 400

    if forecast_days < 1 or forecast_days > 30:
        return jsonify({
            "status": "error",
            "message": "forecast_days must be between 1 and 30"
        }), 400

    try:
        predictions = generate_product_forecast(
            product_id,
            forecast_days
        )

        return jsonify({
            "status": "success",
            "message": "Forecast generated successfully",
            "product_id": product_id,
            "forecast_days": len(predictions),
            "forecasts": predictions
        })

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to generate forecast",
            "details": str(error)
        }), 500


@forecast_api_bp.route(
    "/generate-all",
    methods=["POST"]
)
@business_or_admin_required
def generate_all():
    """Generate forecasts for all eligible products."""

    data = request.get_json(silent=True) or {}

    forecast_days = data.get(
        "forecast_days",
        FORECAST_DAYS
    )

    try:
        forecast_days = int(forecast_days)
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "forecast_days must be an integer"
        }), 400

    if forecast_days < 1 or forecast_days > 30:
        return jsonify({
            "status": "error",
            "message": "forecast_days must be between 1 and 30"
        }), 400

    try:
        result = generate_all_forecasts(
            forecast_days
        )

        return jsonify({
            "status": "success",
            "message": "Forecast generation completed",
            "forecast_days": forecast_days,
            "generated_count": len(result["generated"]),
            "skipped_count": len(result["skipped"]),
            "generated": result["generated"],
            "skipped": result["skipped"]
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to generate forecasts",
            "details": str(error)
        }), 500


@forecast_api_bp.route("/summary", methods=["GET"])
@business_or_admin_required
def forecast_summary():
    """Return forecast summary statistics."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_forecasts,
                COUNT(DISTINCT product_id) AS products_forecasted,
                COALESCE(SUM(predicted_demand), 0)
                    AS total_predicted_demand,
                COALESCE(AVG(predicted_demand), 0)
                    AS average_predicted_demand,
                MIN(forecast_date) AS first_forecast_date,
                MAX(forecast_date) AS last_forecast_date
            FROM forecast
        """)

        summary = cursor.fetchone()

        return jsonify({
            "status": "success",
            "summary": {
                "total_forecasts": int(
                    summary["total_forecasts"]
                ),
                "products_forecasted": int(
                    summary["products_forecasted"]
                ),
                "total_predicted_demand": int(
                    summary["total_predicted_demand"]
                ),
                "average_predicted_demand": round(
                    float(summary["average_predicted_demand"]),
                    2
                ),
                "first_forecast_date": (
                    str(summary["first_forecast_date"])
                    if summary["first_forecast_date"]
                    else None
                ),
                "last_forecast_date": (
                    str(summary["last_forecast_date"])
                    if summary["last_forecast_date"]
                    else None
                )
            }
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve forecast summary",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()