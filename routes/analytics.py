from flask import Blueprint, jsonify, render_template, request

from database import get_connection
from routes.auth import role_required
from services.forecast_service import generate_product_forecast
from services.inventory_intelligence import (
    get_intelligence_summary,
)

analytics_bp = Blueprint("analytics", __name__)


# --------------------------------
# Forecast Dashboard
# --------------------------------

@analytics_bp.route("/forecast")
@role_required("Business", "Admin")
def forecast():
    """
    Render the demand forecast dashboard.

    The actual forecasting logic is handled by forecast_service.py.
    """

    product_id = request.args.get("product_id", type=int)

    prediction = None
    forecasts = []

    if product_id:
        try:
            forecasts = generate_product_forecast(
                product_id,
                forecast_days=7
            )

            if forecasts:
                prediction = forecasts[0]["predicted_demand"]

        except ValueError:
            prediction = None

    return render_template(
        "forecast.html",
        prediction=prediction,
        forecasts=forecasts,
        product_id=product_id
    )


# --------------------------------
# Total Products API
# --------------------------------

@analytics_bp.route("/api/total-products")
@role_required("Business", "Admin")
def total_products():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM products
        """)

        total = cursor.fetchone()[0]

        return jsonify({
            "status": "success",
            "total_products": total
        })

    finally:
        cursor.close()
        connection.close()


# --------------------------------
# Total Revenue API
# --------------------------------

@analytics_bp.route("/api/total-revenue")
@role_required("Business", "Admin")
def total_revenue():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT IFNULL(SUM(revenue), 0)
            FROM sales
        """)

        revenue = cursor.fetchone()[0]

        return jsonify({
            "status": "success",
            "total_revenue": float(revenue)
        })

    finally:
        cursor.close()
        connection.close()


# --------------------------------
# Total Stocks API
# --------------------------------

@analytics_bp.route("/api/total-stocks")
@role_required("Business", "Admin")
def total_stocks():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM stocks
        """)

        total = cursor.fetchone()[0]

        return jsonify({
            "status": "success",
            "total_stocks": total
        })

    finally:
        cursor.close()
        connection.close()


# --------------------------------
# Total Investors API
# --------------------------------

@analytics_bp.route("/api/total-investors")
@role_required("Admin")
def total_investors():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role = 'Investor'
        """)

        total = cursor.fetchone()[0]

        return jsonify({
            "status": "success",
            "total_investors": total
        })

    finally:
        cursor.close()
        connection.close()


# --------------------------------
# Business Analytics Summary
# --------------------------------

@analytics_bp.route("/api/analytics/summary")
@role_required("Business", "Admin")
def analytics_summary():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM products
        """)
        total_products = cursor.fetchone()[0]

        cursor.execute("""
            SELECT IFNULL(SUM(revenue), 0)
            FROM sales
        """)
        total_revenue = cursor.fetchone()[0]

        cursor.execute("""
            SELECT IFNULL(SUM(quantity_sold), 0)
            FROM sales
        """)
        total_units_sold = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM stocks
        """)
        total_stocks = cursor.fetchone()[0]

        intelligence = get_intelligence_summary()

        return jsonify({
            "status": "success",
            "business": {
                "total_products": total_products,
                "total_revenue": float(total_revenue),
                "total_units_sold": int(total_units_sold),
                "total_stocks": total_stocks
            },
            "inventory": intelligence
        })

    finally:
        cursor.close()
        connection.close()