from datetime import date

from database import get_connection


def calculate_inventory_status(
    current_stock,
    predicted_demand,
    reorder_level
):
    """Calculate stock status and recommended reorder quantity."""

    current_stock = int(current_stock)
    predicted_demand = int(predicted_demand)
    reorder_level = int(reorder_level)

    projected_stock = current_stock - predicted_demand

    if current_stock <= 0:
        status = "OUT_OF_STOCK"
        risk = "HIGH"

    elif projected_stock <= 0:
        status = "STOCKOUT_RISK"
        risk = "HIGH"

    elif current_stock <= reorder_level:
        status = "LOW_STOCK"
        risk = "MEDIUM"

    elif projected_stock <= reorder_level:
        status = "REORDER_SOON"
        risk = "MEDIUM"

    else:
        status = "HEALTHY"
        risk = "LOW"

    # Keep enough stock to cover predicted demand
    # while restoring inventory to the reorder level.
    recommended_stock = predicted_demand + reorder_level

    recommended_reorder = max(
        0,
        recommended_stock - current_stock
    )

    return {
        "current_stock": current_stock,
        "predicted_demand": predicted_demand,
        "projected_stock": projected_stock,
        "reorder_level": reorder_level,
        "recommended_reorder": recommended_reorder,
        "status": status,
        "risk": risk
    }


def get_inventory_intelligence():
    """
    Combine inventory data with the latest forecast
    for each product and branch.
    """

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

                COALESCE(
                    (
                        SELECT SUM(f.predicted_demand)
                        FROM forecast f
                        WHERE f.product_id = i.product_id
                          AND f.forecast_date >= CURDATE()
                    ),
                    0
                ) AS predicted_demand

            FROM inventory i

            INNER JOIN products p
                ON i.product_id = p.product_id

            INNER JOIN branches b
                ON i.branch_id = b.branch_id

            ORDER BY i.product_id, i.branch_id
        """)

        rows = cursor.fetchall()

        intelligence = []

        for row in rows:

            analysis = calculate_inventory_status(
                row["stock_quantity"],
                row["predicted_demand"],
                row["reorder_level"]
            )

            intelligence.append({
                "inventory_id": row["inventory_id"],
                "product_id": row["product_id"],
                "sku": row["sku"],
                "product_name": row["product_name"],
                "category": row["category"],
                "branch_id": row["branch_id"],
                "branch_name": row["branch_name"],
                **analysis
            })

        return intelligence

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_product_intelligence(product_id):
    """Return inventory intelligence for one product."""

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

                COALESCE(
                    (
                        SELECT SUM(f.predicted_demand)
                        FROM forecast f
                        WHERE f.product_id = i.product_id
                          AND f.forecast_date >= CURDATE()
                    ),
                    0
                ) AS predicted_demand

            FROM inventory i

            INNER JOIN products p
                ON i.product_id = p.product_id

            INNER JOIN branches b
                ON i.branch_id = b.branch_id

            WHERE i.product_id = %s

            ORDER BY i.branch_id
        """, (product_id,))

        rows = cursor.fetchall()

        if not rows:
            return None

        intelligence = []

        for row in rows:

            analysis = calculate_inventory_status(
                row["stock_quantity"],
                row["predicted_demand"],
                row["reorder_level"]
            )

            intelligence.append({
                "inventory_id": row["inventory_id"],
                "product_id": row["product_id"],
                "sku": row["sku"],
                "product_name": row["product_name"],
                "category": row["category"],
                "branch_id": row["branch_id"],
                "branch_name": row["branch_name"],
                **analysis
            })

        return intelligence

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_inventory_alerts():
    """Return only inventory records requiring attention."""

    intelligence = get_inventory_intelligence()

    alerts = [
        item
        for item in intelligence
        if item["status"] != "HEALTHY"
    ]

    # Highest risk first.
    risk_order = {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 2
    }

    alerts.sort(
        key=lambda item: (
            risk_order.get(item["risk"], 99),
            -item["recommended_reorder"]
        )
    )

    return alerts


def get_intelligence_summary():
    """Return overall inventory intelligence statistics."""

    intelligence = get_inventory_intelligence()

    summary = {
        "total_items": len(intelligence),
        "healthy_items": 0,
        "low_stock_items": 0,
        "reorder_soon_items": 0,
        "stockout_risk_items": 0,
        "out_of_stock_items": 0,
        "high_risk_items": 0,
        "medium_risk_items": 0,
        "recommended_reorder_units": 0
    }

    for item in intelligence:

        status = item["status"]
        risk = item["risk"]

        if status == "HEALTHY":
            summary["healthy_items"] += 1

        elif status == "LOW_STOCK":
            summary["low_stock_items"] += 1

        elif status == "REORDER_SOON":
            summary["reorder_soon_items"] += 1

        elif status == "STOCKOUT_RISK":
            summary["stockout_risk_items"] += 1

        elif status == "OUT_OF_STOCK":
            summary["out_of_stock_items"] += 1

        if risk == "HIGH":
            summary["high_risk_items"] += 1

        elif risk == "MEDIUM":
            summary["medium_risk_items"] += 1

        summary["recommended_reorder_units"] += (
            item["recommended_reorder"]
        )

    return summary