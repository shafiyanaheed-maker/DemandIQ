import mysql.connector


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Dolly#122006",
    "database": "demandiq",
}


# Expected minimum/fixed counts
EXPECTED_PRODUCTS = 95
EXPECTED_INVENTORY = 570
EXPECTED_SUPPLIERS = 30
EXPECTED_BRANCHES = 6
EXPECTED_SALES = 34675
EXPECTED_STOCKS = 5
EXPECTED_MARKET_DATA = 1825


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# TABLE COUNT
# ============================================================

def get_count(cursor, table_name):
    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    return cursor.fetchone()[0]


# ============================================================
# RELATIONSHIP CHECKS
# ============================================================

def check_sales_products(cursor):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales s
        LEFT JOIN products p
            ON s.product_id = p.product_id
        WHERE p.product_id IS NULL
        """
    )

    return cursor.fetchone()[0]


def check_inventory_products(cursor):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM inventory i
        LEFT JOIN products p
            ON i.product_id = p.product_id
        WHERE p.product_id IS NULL
        """
    )

    return cursor.fetchone()[0]


def check_inventory_branches(cursor):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM inventory i
        LEFT JOIN branches b
            ON i.branch_id = b.branch_id
        WHERE b.branch_id IS NULL
        """
    )

    return cursor.fetchone()[0]


def check_market_stocks(cursor):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM market_data m
        LEFT JOIN stocks s
            ON m.stock_id = s.stock_id
        WHERE s.stock_id IS NULL
        """
    )

    return cursor.fetchone()[0]


# ============================================================
# DUPLICATE CHECKS
# ============================================================

def check_sales_duplicates(cursor):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT product_id, sale_date
            FROM sales
            GROUP BY product_id, sale_date
            HAVING COUNT(*) > 1
        ) duplicates
        """
    )

    return cursor.fetchone()[0]


def check_market_duplicates(cursor):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT stock_id, data_date
            FROM market_data
            GROUP BY stock_id, data_date
            HAVING COUNT(*) > 1
        ) duplicates
        """
    )

    return cursor.fetchone()[0]


# ============================================================
# MAIN
# ============================================================

def main():

    print("DemandIQ Database & Dataset Audit")
    print("=" * 60)

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # TABLE COUNTS
    # --------------------------------------------------------

    products = get_count(
        cursor,
        "products"
    )

    inventory = get_count(
        cursor,
        "inventory"
    )

    suppliers = get_count(
        cursor,
        "suppliers"
    )

    branches = get_count(
        cursor,
        "branches"
    )

    sales = get_count(
        cursor,
        "sales"
    )

    stocks = get_count(
        cursor,
        "stocks"
    )

    market_data = get_count(
        cursor,
        "market_data"
    )

    print()
    print("TABLE COUNTS")
    print("-" * 60)

    print(
        f"Products       : {products}"
    )

    print(
        f"Inventory      : {inventory}"
    )

    print(
        f"Suppliers      : {suppliers}"
    )

    print(
        f"Branches       : {branches}"
    )

    print(
        f"Sales          : {sales}"
    )

    print(
        f"Stocks         : {stocks}"
    )

    print(
        f"Market Data    : {market_data}"
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    sales_orphans = check_sales_products(
        cursor
    )

    inventory_product_orphans = (
        check_inventory_products(cursor)
    )

    inventory_branch_orphans = (
        check_inventory_branches(cursor)
    )

    market_orphans = check_market_stocks(
        cursor
    )

    print()
    print("RELATIONSHIP CHECKS")
    print("-" * 60)

    print(
        f"Sales → Products          : "
        f"{sales_orphans} orphan records"
    )

    print(
        f"Inventory → Products      : "
        f"{inventory_product_orphans} orphan records"
    )

    print(
        f"Inventory → Branches      : "
        f"{inventory_branch_orphans} orphan records"
    )

    print(
        f"Market Data → Stocks      : "
        f"{market_orphans} orphan records"
    )

    # --------------------------------------------------------
    # DUPLICATES
    # --------------------------------------------------------

    sales_duplicates = check_sales_duplicates(
        cursor
    )

    market_duplicates = check_market_duplicates(
        cursor
    )

    print()
    print("DUPLICATE CHECKS")
    print("-" * 60)

    print(
        f"Sales product/date duplicates : "
        f"{sales_duplicates}"
    )

    print(
        f"Market stock/date duplicates  : "
        f"{market_duplicates}"
    )

    # --------------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------------

    all_counts_valid = (
        products == EXPECTED_PRODUCTS
        and inventory == EXPECTED_INVENTORY
        and suppliers == EXPECTED_SUPPLIERS
        and branches == EXPECTED_BRANCHES
        and sales == EXPECTED_SALES
        and stocks == EXPECTED_STOCKS
        and market_data == EXPECTED_MARKET_DATA
    )

    all_relationships_valid = (
        sales_orphans == 0
        and inventory_product_orphans == 0
        and inventory_branch_orphans == 0
        and market_orphans == 0
    )

    all_duplicates_valid = (
        sales_duplicates == 0
        and market_duplicates == 0
    )

    print()
    print("=" * 60)

    if (
        all_counts_valid
        and all_relationships_valid
        and all_duplicates_valid
    ):

        print(
            "🎉 DATABASE & DATASET AUDIT PASSED"
        )

        print()
        print(
            "DemandIQ data foundation is complete."
        )

    else:

        print(
            "⚠️ DATABASE & DATASET AUDIT "
            "NEEDS ATTENTION"
        )

        if not all_counts_valid:
            print(
                "❌ One or more table counts "
                "do not match expectations."
            )

        if not all_relationships_valid:
            print(
                "❌ One or more table relationships "
                "contain orphan records."
            )

        if not all_duplicates_valid:
            print(
                "❌ Duplicate records were detected."
            )

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()