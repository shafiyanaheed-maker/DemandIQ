from functools import wraps

from flask import Blueprint, jsonify, request, session

from database import get_connection


product_api_bp = Blueprint("product_api", __name__, url_prefix="/api/products")


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


@product_api_bp.route("", methods=["GET"])
@business_or_admin_required
def get_products():
    """
    Return all products with supplier information.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.sku,
                p.product_name,
                p.brand,
                p.category,
                p.sub_category,
                p.description,
                p.supplier_id,
                s.supplier_name,
                p.cost_price,
                p.selling_price,
                p.stock_quantity,
                p.created_at
            FROM products p
            LEFT JOIN suppliers s
                ON p.supplier_id = s.supplier_id
            ORDER BY p.product_id
        """)

        products = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(products),
            "products": products
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve products",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@product_api_bp.route("/<int:product_id>", methods=["GET"])
@business_or_admin_required
def get_product(product_id):
    """
    Return one product by ID.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.sku,
                p.product_name,
                p.brand,
                p.category,
                p.sub_category,
                p.description,
                p.supplier_id,
                s.supplier_name,
                p.cost_price,
                p.selling_price,
                p.stock_quantity,
                p.created_at
            FROM products p
            LEFT JOIN suppliers s
                ON p.supplier_id = s.supplier_id
            WHERE p.product_id = %s
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404

        return jsonify({
            "status": "success",
            "product": product
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve product",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@product_api_bp.route("", methods=["POST"])
@business_or_admin_required
def create_product():
    """
    Create a new product.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON request body is required"
        }), 400

    required_fields = [
        "sku",
        "product_name",
        "brand",
        "category",
        "sub_category",
        "supplier_id",
        "cost_price",
        "selling_price",
        "stock_quantity"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "status": "error",
            "message": "Missing required fields",
            "fields": missing_fields
        }), 400

    if data["cost_price"] < 0 or data["selling_price"] < 0:
        return jsonify({
            "status": "error",
            "message": "Prices cannot be negative"
        }), 400

    if data["stock_quantity"] < 0:
        return jsonify({
            "status": "error",
            "message": "Stock quantity cannot be negative"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT product_id
            FROM products
            WHERE sku = %s
        """, (data["sku"],))

        if cursor.fetchone():
            return jsonify({
                "status": "error",
                "message": "SKU already exists"
            }), 409

        cursor.execute("""
            INSERT INTO products (
                sku,
                product_name,
                brand,
                category,
                sub_category,
                description,
                supplier_id,
                cost_price,
                selling_price,
                stock_quantity
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["sku"],
            data["product_name"],
            data["brand"],
            data["category"],
            data["sub_category"],
            data.get("description", ""),
            data["supplier_id"],
            data["cost_price"],
            data["selling_price"],
            data["stock_quantity"]
        ))

        connection.commit()

        product_id = cursor.lastrowid

        return jsonify({
            "status": "success",
            "message": "Product created successfully",
            "product_id": product_id
        }), 201

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "status": "error",
            "message": "Failed to create product",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@product_api_bp.route("/<int:product_id>", methods=["DELETE"])
@business_or_admin_required
def delete_product(product_id):
    """
    Delete a product.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT product_id
            FROM products
            WHERE product_id = %s
        """, (product_id,))

        if not cursor.fetchone():
            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = %s
        """, (product_id,))

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Product deleted successfully"
        })

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "status": "error",
            "message": "Product could not be deleted",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()