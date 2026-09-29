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

DATASET_FILE = Path("data/market_data.csv")


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_valid_stock_ids(connection):
    """Get stock IDs that currently exist in the database."""

    cursor = connection.cursor()

    cursor.execute(
        "SELECT stock_id FROM stocks"
    )

    stock_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    cursor.close()

    return stock_ids


def get_existing_market_count(connection):
    """Return the current number of market_data records."""

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM market_data"
    )

    count = cursor.fetchone()[0]

    cursor.close()

    return count


# ============================================================
# CSV
# ============================================================

def load_dataset():

    if not DATASET_FILE.exists():

        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    with open(
        DATASET_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


# ============================================================
# SEEDING
# ============================================================

def seed_market_data(
    connection,
    records,
    valid_stock_ids
):
    """Insert market records into MySQL."""

    insert_query = """
        INSERT INTO market_data (
            stock_id,
            data_date,
            open_price,
            close_price,
            volume
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    rows_to_insert = []

    skipped = 0

    for row in records:

        stock_id = int(
            row["stock_id"]
        )

        if stock_id not in valid_stock_ids:

            skipped += 1
            continue

        rows_to_insert.append(
            (
                stock_id,
                row["data_date"],
                float(row["open_price"]),
                float(row["close_price"]),
                int(row["volume"]),
            )
        )

    cursor = connection.cursor()

    cursor.executemany(
        insert_query,
        rows_to_insert
    )

    connection.commit()

    inserted = cursor.rowcount

    cursor.close()

    return inserted, skipped


# ============================================================
# SUMMARY
# ============================================================

def get_market_summary(connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS records,
            COUNT(DISTINCT stock_id) AS stocks,
            MIN(data_date) AS first_date,
            MAX(data_date) AS last_date,
            ROUND(AVG(close_price), 2) AS avg_close,
            SUM(volume) AS total_volume
        FROM market_data
        """
    )

    summary = cursor.fetchone()

    cursor.close()

    return summary


# ============================================================
# MAIN
# ============================================================

def main():

    print("DemandIQ Market Data Seeder")
    print("=" * 45)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    records = load_dataset()

    print(
        f"CSV records found: {len(records)}"
    )

    if not records:

        print(
            "ERROR: Market dataset is empty."
        )

        return

    # --------------------------------------------------------
    # Connect
    # --------------------------------------------------------

    connection = get_connection()

    try:

        print("Connected to MySQL.")

        # ----------------------------------------------------
        # Safety check
        # ----------------------------------------------------

        existing_count = (
            get_existing_market_count(
                connection
            )
        )

        print(
            f"Existing market_data records: "
            f"{existing_count}"
        )

        if existing_count > 0:

            print()
            print(
                "⚠️ market_data already contains "
                "records."
            )

            print(
                "Seeding stopped to prevent "
                "duplicate data."
            )

            print(
                "Clear the existing market_data "
                "only if you intentionally want "
                "to reseed it."
            )

            return

        # ----------------------------------------------------
        # Stocks
        # ----------------------------------------------------

        valid_stock_ids = (
            fetch_valid_stock_ids(
                connection
            )
        )

        print(
            f"Valid stocks in database: "
            f"{len(valid_stock_ids)}"
        )

        # ----------------------------------------------------
        # Seed
        # ----------------------------------------------------

        inserted, skipped = seed_market_data(
            connection,
            records,
            valid_stock_ids
        )

        print()
        print("SEEDING RESULTS")
        print("-" * 45)

        print(
            f"Records inserted: {inserted}"
        )

        print(
            f"Records skipped: {skipped}"
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        summary = get_market_summary(
            connection
        )

        print()
        print("DATABASE SUMMARY")
        print("-" * 45)

        print(
            f"Total market records: {summary[0]}"
        )

        print(
            f"Stocks with data: {summary[1]}"
        )

        print(
            f"First market date: {summary[2]}"
        )

        print(
            f"Last market date: {summary[3]}"
        )

        print(
            f"Average close price: {summary[4]}"
        )

        print(
            f"Total trading volume: {summary[5]}"
        )

        print()
        print(
            "🎉 MARKET DATA SEEDED SUCCESSFULLY"
        )

    except Exception as error:

        connection.rollback()

        print()
        print("❌ SEEDING FAILED")
        print(f"Error: {error}")

    finally:

        connection.close()

        print(
            "Database connection closed."
        )


if __name__ == "__main__":
    main()