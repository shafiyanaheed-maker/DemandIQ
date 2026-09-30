from functools import wraps

from flask import Blueprint, jsonify, request, session

from database import get_connection


inventory_api_bp = Blueprint(
    "inventory_api",
    __name__,
    url_prefix="/api/inventory"
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


@inventory_api_bp.route("", methods=["GET"])
@business_or_admin_required
def get_inventory():
    """Return inventory for all products and branches."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                i.inventory_id,
                i.product_id,
                p.sku,
                p.product_name,
                p.category,
                i.branch_id,
                b.branch_name,
                i.stock_quantity,
                i.reorder_level,
                i.last_updated
            FROM inventory i
            INNER JOIN products p
                ON i.product_id = p.product_id
            INNER JOIN branches b
                ON i.branch_id = b.branch_id
            ORDER BY i.last_updated DESC, i.inventory_id DESC
        """)

        inventory = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(inventory),
            "inventory": inventory
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve inventory",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@inventory_api_bp.route("/<int:inventory_id>", methods=["GET"])
@business_or_admin_required
def get_inventory_item(inventory_id):
    """Return one inventory record."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                i.inventory_id,
                i.product_id,
                p.sku,
                p.product_name,
                p.category,
                i.branch_id,
                b.branch_name,
                i.stock_quantity,
                i.reorder_level,
                i.last_updated
            FROM inventory i
            INNER JOIN products p
                ON i.product_id = p.product_id
            INNER JOIN branches b
                ON i.branch_id = b.branch_id
            WHERE i.inventory_id = %s
        """, (inventory_id,))

        item = cursor.fetchone()

        if not item:
            return jsonify({
                "status": "error",
                "message": "Inventory record not found"
            }), 404

        return jsonify({
            "status": "success",
            "inventory": item
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve inventory record",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@inventory_api_bp.route("/product/<int:product_id>", methods=["GET"])
@business_or_admin_required
def get_product_inventory(product_id):
    """Return inventory for a product across all branches."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                i.inventory_id,
                i.product_id,
                p.sku,
                p.product_name,
                i.branch_id,
                b.branch_name,
                i.stock_quantity,
                i.reorder_level,
                i.last_updated
            FROM inventory i
            INNER JOIN products p
                ON i.product_id = p.product_id
            INNER JOIN branches b
                ON i.branch_id = b.branch_id
            WHERE i.product_id = %s
            ORDER BY b.branch_id
        """, (product_id,))

        inventory = cursor.fetchall()

        if not inventory:
            return jsonify({
                "status": "error",
                "message": "No inventory found for this product"
            }), 404

        return jsonify({
            "status": "success",
            "count": len(inventory),
            "inventory": inventory
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve product inventory",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@inventory_api_bp.route("/branch/<int:branch_id>", methods=["GET"])
@business_or_admin_required
def get_branch_inventory(branch_id):
    """Return inventory for a specific branch."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                i.inventory_id,
                i.product_id,
                p.sku,
                p.product_name,
                p.category,
                i.branch_id,
                b.branch_name,
                i.stock_quantity,
                i.reorder_level,
                i.last_updated
            FROM inventory i
            INNER JOIN products p
                ON i.product_id = p.product_id
            INNER JOIN branches b
                ON i.branch_id = b.branch_id
            WHERE i.branch_id = %s
            ORDER BY p.product_name
        """, (branch_id,))

        inventory = cursor.fetchall()

        if not inventory:
            return jsonify({
                "status": "error",
                "message": "No inventory found for this branch"
            }), 404

        return jsonify({
            "status": "success",
            "count": len(inventory),
            "inventory": inventory
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve branch inventory",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@inventory_api_bp.route("/low-stock", methods=["GET"])
@business_or_admin_required
def get_low_stock():
    """Return products whose branch stock is at or below reorder level."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                i.inventory_id,
                i.product_id,
                p.sku,
                p.product_name,
                p.category,
                i.branch_id,
                b.branch_name,
                i.stock_quantity,
                i.reorder_level,
                (i.reorder_level - i.stock_quantity) AS shortage,
                i.last_updated
            FROM inventory i
            INNER JOIN products p
                ON i.product_id = p.product_id
            INNER JOIN branches b
                ON i.branch_id = b.branch_id
            WHERE i.stock_quantity <= i.reorder_level
            ORDER BY shortage DESC, i.stock_quantity ASC
        """)

        low_stock = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(low_stock),
            "low_stock": low_stock
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve low-stock inventory",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@inventory_api_bp.route("/summary", methods=["GET"])
@business_or_admin_required
def inventory_summary():
    """Return overall inventory statistics."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_inventory_records,
                COALESCE(SUM(stock_quantity), 0) AS total_units,
                COALESCE(SUM(
                    CASE
                        WHEN stock_quantity <= reorder_level THEN 1
                        ELSE 0
                    END
                ), 0) AS low_stock_items,
                COUNT(DISTINCT product_id) AS products_tracked,
                COUNT(DISTINCT branch_id) AS branches_tracked
            FROM inventory
        """)

        summary = cursor.fetchone()

        return jsonify({
            "status": "success",
            "summary": {
                "total_inventory_records": int(
                    summary["total_inventory_records"]
                ),
                "total_units": int(summary["total_units"]),
                "low_stock_items": int(summary["low_stock_items"]),
                "products_tracked": int(summary["products_tracked"]),
                "branches_tracked": int(summary["branches_tracked"])
            }
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve inventory summary",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@inventory_api_bp.route("/<int:inventory_id>", methods=["PUT"])
@business_or_admin_required
def update_inventory(inventory_id):
    """Update stock quantity and reorder level for an inventory record."""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON request body is required"
        }), 400

    if "stock_quantity" not in data and "reorder_level" not in data:
        return jsonify({
            "status": "error",
            "message": "Provide stock_quantity or reorder_level"
        }), 400

    stock_quantity = data.get("stock_quantity")
    reorder_level = data.get("reorder_level")

    try:
        if stock_quantity is not None:
            stock_quantity = int(stock_quantity)

        if reorder_level is not None:
            reorder_level = int(reorder_level)

    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "Stock quantity and reorder level must be integers"
        }), 400

    if stock_quantity is not None and stock_quantity < 0:
        return jsonify({
            "status": "error",
            "message": "Stock quantity cannot be negative"
        }), 400

    if reorder_level is not None and reorder_level < 0:
        return jsonify({
            "status": "error",
            "message": "Reorder level cannot be negative"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT inventory_id, stock_quantity, reorder_level
            FROM inventory
            WHERE inventory_id = %s
            FOR UPDATE
        """, (inventory_id,))

        existing = cursor.fetchone()

        if not existing:
            connection.rollback()

            return jsonify({
                "status": "error",
                "message": "Inventory record not found"
            }), 404

        new_stock = (
            stock_quantity
            if stock_quantity is not None
            else existing["stock_quantity"]
        )

        new_reorder = (
            reorder_level
            if reorder_level is not None
            else existing["reorder_level"]
        )

        cursor.execute("""
            UPDATE inventory
            SET
                stock_quantity = %s,
                reorder_level = %s,
                last_updated = CURRENT_TIMESTAMP
            WHERE inventory_id = %s
        """, (
            new_stock,
            new_reorder,
            inventory_id
        ))

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Inventory updated successfully",
            "inventory": {
                "inventory_id": inventory_id,
                "stock_quantity": new_stock,
                "reorder_level": new_reorder
            }
        })

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "status": "error",
            "message": "Failed to update inventory",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()