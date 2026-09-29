import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Dolly#122006",
    "database": "demandiq",
}


EXPECTED_SALES_RECORDS = 34675
EXPECTED_PRODUCTS = 95


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def main():
    connection = get_connection()
    cursor = connection.cursor()

    print("DemandIQ Sales Data Verification")
    print("=" * 45)

    # --------------------------------------------------------
    # Total sales records
    # --------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM sales")
    total = cursor.fetchone()[0]

    print(f"Total sales records : {total}")

    # --------------------------------------------------------
    # Products with sales
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(DISTINCT product_id) FROM sales"
    )
    products = cursor.fetchone()[0]

    print(f"Products with sales : {products}")

    # --------------------------------------------------------
    # Date range
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT MIN(sale_date), MAX(sale_date)
        FROM sales
        """
    )

    first_date, last_date = cursor.fetchone()

    print(f"First sale date     : {first_date}")
    print(f"Last sale date      : {last_date}")

    # --------------------------------------------------------
    # Total units sold
    # --------------------------------------------------------

    cursor.execute(
        "SELECT SUM(quantity_sold) FROM sales"
    )

    units = cursor.fetchone()[0]

    print(f"Total units sold    : {units}")

    # --------------------------------------------------------
    # Total revenue
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT ROUND(SUM(revenue), 2)
        FROM sales
        """
    )

    revenue = cursor.fetchone()[0]

    print(f"Total revenue       : {revenue}")

    # --------------------------------------------------------
    # Duplicate records
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT product_id, sale_date, COUNT(*)
        FROM sales
        GROUP BY product_id, sale_date
        HAVING COUNT(*) > 1
        """
    )

    duplicates = cursor.fetchall()

    print(f"Duplicate records   : {len(duplicates)}")

    # --------------------------------------------------------
    # Invalid quantities
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales
        WHERE quantity_sold <= 0
        """
    )

    invalid_quantity = cursor.fetchone()[0]

    print(f"Invalid quantities   : {invalid_quantity}")

    # --------------------------------------------------------
    # Invalid revenue
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales
        WHERE revenue <= 0
        """
    )

    invalid_revenue = cursor.fetchone()[0]

    print(f"Invalid revenue     : {invalid_revenue}")

    # --------------------------------------------------------
    # Product relationship check
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(DISTINCT s.product_id)
        FROM sales s
        INNER JOIN products p
            ON s.product_id = p.product_id
        """
    )

    linked_products = cursor.fetchone()[0]

    print(f"Linked products     : {linked_products}")

    # --------------------------------------------------------
    # Final verification
    # --------------------------------------------------------

    print()
    print("=" * 45)

    if (
        total == EXPECTED_SALES_RECORDS
        and products == EXPECTED_PRODUCTS
        and linked_products == EXPECTED_PRODUCTS
        and len(duplicates) == 0
        and invalid_quantity == 0
        and invalid_revenue == 0
    ):
        print("🎉 SALES DATABASE VERIFICATION PASSED")
        print()
        print("Sales dataset is ready for DemandIQ.")
    else:
        print("⚠️ VERIFICATION NEEDS ATTENTION")

        print()
        print("Expected:")
        print(f"  Sales records : {EXPECTED_SALES_RECORDS}")
        print(f"  Products      : {EXPECTED_PRODUCTS}")

        print()
        print("Actual:")
        print(f"  Sales records : {total}")
        print(f"  Products      : {products}")
        print(f"  Linked        : {linked_products}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()