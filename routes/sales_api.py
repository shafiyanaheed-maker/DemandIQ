from functools import wraps

from flask import Blueprint, jsonify, request, session

from database import get_connection


sales_api_bp = Blueprint(
    "sales_api",
    __name__,
    url_prefix="/api/sales"
)


def business_or_admin_required(view_function):
    """
    Allow only authenticated Business or Admin users.
    """

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


@sales_api_bp.route("", methods=["GET"])
@business_or_admin_required
def get_sales():
    """
    Return sales records with product information.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                s.sale_id,
                s.product_id,
                p.sku,
                p.product_name,
                s.sale_date,
                s.quantity_sold,
                s.revenue
            FROM sales s
            INNER JOIN products p
                ON s.product_id = p.product_id
            ORDER BY s.sale_date DESC, s.sale_id DESC
        """)

        sales = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(sales),
            "sales": sales
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve sales",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@sales_api_bp.route("/<int:sale_id>", methods=["GET"])
@business_or_admin_required
def get_sale(sale_id):
    """
    Return one sale by ID.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                s.sale_id,
                s.product_id,
                p.sku,
                p.product_name,
                s.sale_date,
                s.quantity_sold,
                s.revenue
            FROM sales s
            INNER JOIN products p
                ON s.product_id = p.product_id
            WHERE s.sale_id = %s
        """, (sale_id,))

        sale = cursor.fetchone()

        if not sale:
            return jsonify({
                "status": "error",
                "message": "Sale not found"
            }), 404

        return jsonify({
            "status": "success",
            "sale": sale
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve sale",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@sales_api_bp.route("", methods=["POST"])
@business_or_admin_required
def create_sale():
    """
    Record a new sale and reduce product stock.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON request body is required"
        }), 400

    required_fields = [
        "product_id",
        "quantity_sold"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "status": "error",
            "message": "Missing required fields",
            "fields": missing_fields
        }), 400

    try:
        product_id = int(data["product_id"])
        quantity_sold = int(data["quantity_sold"])
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "product_id and quantity_sold must be integers"
        }), 400

    if product_id <= 0:
        return jsonify({
            "status": "error",
            "message": "product_id must be greater than zero"
        }), 400

    if quantity_sold <= 0:
        return jsonify({
            "status": "error",
            "message": "quantity_sold must be greater than zero"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Lock the product row while processing the sale.
        cursor.execute("""
            SELECT
                product_id,
                selling_price,
                stock_quantity
            FROM products
            WHERE product_id = %s
            FOR UPDATE
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            connection.rollback()

            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404

        current_stock = int(product["stock_quantity"])

        if current_stock < quantity_sold:
            connection.rollback()

            return jsonify({
                "status": "error",
                "message": "Insufficient stock",
                "available_stock": current_stock,
                "requested_quantity": quantity_sold
            }), 409

        selling_price = float(product["selling_price"])
        revenue = selling_price * quantity_sold

        # Record the sale.
        cursor.execute("""
            INSERT INTO sales (
                product_id,
                sale_date,
                quantity_sold,
                revenue
            )
            VALUES (
                %s,
                CURDATE(),
                %s,
                %s
            )
        """, (
            product_id,
            quantity_sold,
            revenue
        ))

        sale_id = cursor.lastrowid

        # Reduce product-level stock.
        new_stock = current_stock - quantity_sold

        cursor.execute("""
            UPDATE products
            SET stock_quantity = %s
            WHERE product_id = %s
        """, (
            new_stock,
            product_id
        ))

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Sale recorded successfully",
            "sale": {
                "sale_id": sale_id,
                "product_id": product_id,
                "quantity_sold": quantity_sold,
                "revenue": round(revenue, 2),
                "remaining_stock": new_stock
            }
        }), 201

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "status": "error",
            "message": "Failed to record sale",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@sales_api_bp.route("/summary", methods=["GET"])
@business_or_admin_required
def sales_summary():
    """
    Return overall sales statistics.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_sales,
                COALESCE(SUM(quantity_sold), 0) AS total_units_sold,
                COALESCE(SUM(revenue), 0) AS total_revenue,
                COUNT(DISTINCT product_id) AS products_sold
            FROM sales
        """)

        summary = cursor.fetchone()

        return jsonify({
            "status": "success",
            "summary": {
                "total_sales": int(summary["total_sales"]),
                "total_units_sold": int(summary["total_units_sold"]),
                "total_revenue": round(float(summary["total_revenue"]), 2),
                "products_sold": int(summary["products_sold"])
            }
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve sales summary",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()