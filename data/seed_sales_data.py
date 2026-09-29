
import csv
from pathlib import Path

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

DATASET_FILE = Path("data/sales_dataset.csv")


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_valid_product_ids(connection):
    """Return product IDs that currently exist in the database."""
    cursor = connection.cursor()

    cursor.execute("SELECT product_id FROM products")

    product_ids = {row[0] for row in cursor.fetchall()}

    cursor.close()

    return product_ids


# ============================================================
# CSV LOADING
# ============================================================

def load_dataset():
    """Load sales records from the generated CSV file."""

    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    with open(
        DATASET_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        return list(reader)


# ============================================================
# DATABASE INSERTION
# ============================================================

def seed_sales_data(connection, records, valid_product_ids):
    """Insert sales records into the sales table."""

    insert_query = """
        INSERT INTO sales (
            product_id,
            sale_date,
            quantity_sold,
            revenue
        )
        VALUES (%s, %s, %s, %s)
    """

    rows_to_insert = []

    skipped = 0

    for row in records:

        product_id = int(row["product_id"])

        # Safety check: never insert a sales record
        # for a product that does not exist.
        if product_id not in valid_product_ids:
            skipped += 1
            continue

        rows_to_insert.append(
            (
                product_id,
                row["sale_date"],
                int(row["quantity_sold"]),
                float(row["revenue"]),
            )
        )

    cursor = connection.cursor()

    cursor.executemany(
        insert_query,
        rows_to_insert,
    )

    connection.commit()

    inserted = cursor.rowcount

    cursor.close()

    return inserted, skipped


# ============================================================
# VERIFICATION
# ============================================================

def get_sales_count(connection):
    """Return the total number of sales records."""
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales")

    count = cursor.fetchone()[0]

    cursor.close()

    return count


def get_sales_summary(connection):
    """Display a small summary of the seeded sales data."""

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS records,
            COUNT(DISTINCT product_id) AS products,
            MIN(sale_date) AS first_date,
            MAX(sale_date) AS last_date,
            SUM(quantity_sold) AS units,
            ROUND(SUM(revenue), 2) AS revenue
        FROM sales
        """
    )

    summary = cursor.fetchone()

    cursor.close()

    return summary


# ============================================================
# MAIN
# ============================================================

def main():

    print("DemandIQ Sales Data Seeder")
    print("=" * 40)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    records = load_dataset()

    print(f"CSV records found: {len(records)}")

    if not records:
        print("ERROR: Dataset is empty.")
        return

    # --------------------------------------------------------
    # Connect to MySQL
    # --------------------------------------------------------

    connection = get_connection()

    try:

        print("Connected to MySQL.")

        # ----------------------------------------------------
        # Check products
        # ----------------------------------------------------

        valid_product_ids = fetch_valid_product_ids(connection)

        print(
            f"Valid products in database: "
            f"{len(valid_product_ids)}"
        )

        # ----------------------------------------------------
        # Seed
        # ----------------------------------------------------

        inserted, skipped = seed_sales_data(
            connection,
            records,
            valid_product_ids,
        )

        print()
        print("SEEDING RESULTS")
        print("-" * 40)
        print(f"Records inserted: {inserted}")
        print(f"Records skipped: {skipped}")

        # ----------------------------------------------------
        # Verify
        # ----------------------------------------------------

        total = get_sales_count(connection)

        summary = get_sales_summary(connection)

        print()
        print("DATABASE SUMMARY")
        print("-" * 40)
        print(f"Total sales records: {total}")
        print(f"Products with sales: {summary[1]}")
        print(f"First sale date: {summary[2]}")
        print(f"Last sale date: {summary[3]}")
        print(f"Total units sold: {summary[4]}")
        print(f"Total revenue: {summary[5]}")

        print()
        print("🎉 SALES DATA SEEDED SUCCESSFULLY")

    except Exception as error:

        connection.rollback()

        print()
        print("❌ SEEDING FAILED")
        print(f"Error: {error}")

    finally:

        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()