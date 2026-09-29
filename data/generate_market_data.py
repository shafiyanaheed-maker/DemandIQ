import csv
import random
from datetime import date, timedelta
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

OUTPUT_FILE = Path("data/market_data.csv")

DAYS_TO_GENERATE = 365

START_DATE = date.today() - timedelta(days=DAYS_TO_GENERATE - 1)

RANDOM_SEED = 42


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_stocks(connection):
    """Fetch existing stocks from the database."""

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            stock_id,
            company_name,
            symbol,
            sector,
            current_price
        FROM stocks
        ORDER BY stock_id
        """
    )

    stocks = cursor.fetchall()

    cursor.close()

    return stocks


# ============================================================
# MARKET DATA GENERATION
# ============================================================

def generate_market_data(stocks):
    """
    Generate realistic synthetic historical market data.

    Each stock receives:
        - Open price
        - Close price
        - Trading volume

    Prices move gradually rather than randomly jumping
    between unrelated values.
    """

    random.seed(RANDOM_SEED)

    records = []

    for stock in stocks:

        stock_id = stock["stock_id"]
        symbol = stock["symbol"]
        current_price = float(stock["current_price"])

        # Use current price as the approximate final price
        # and generate historical prices backwards.
        price = current_price

        # Stable stock-specific behavior
        stock_factor = 0.8 + (
            (stock_id * 17) % 40
        ) / 100

        for day_offset in range(DAYS_TO_GENERATE - 1, -1, -1):

            market_date = date.today() - timedelta(
                days=day_offset
            )

            # Daily market movement
            daily_change = random.uniform(
                -0.025,
                0.025
            )

            # Small stock-specific trend
            trend = (
                (stock_factor - 1.0)
                * 0.002
            )

            previous_close = price

            open_price = previous_close * (
                1 + random.uniform(-0.008, 0.008)
            )

            close_price = open_price * (
                1 + daily_change + trend
            )

            # Prevent unrealistic negative/very-low prices
            close_price = max(
                close_price,
                current_price * 0.35
            )

            open_price = max(
                open_price,
                current_price * 0.35
            )

            # Volume depends partly on price movement
            movement = abs(
                close_price - open_price
            ) / open_price

            base_volume = random.randint(
                50000,
                500000
            )

            volume = int(
                base_volume
                * (1 + movement * 8)
            )

            records.append(
                {
                    "stock_id": stock_id,
                    "data_date": market_date,
                    "open_price": round(
                        open_price,
                        2
                    ),
                    "close_price": round(
                        close_price,
                        2
                    ),
                    "volume": volume,
                }
            )

            price = close_price

        print(
            f"Generated {DAYS_TO_GENERATE} days "
            f"for {symbol}"
        )

    return records


# ============================================================
# CSV OUTPUT
# ============================================================

def save_dataset(records):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "stock_id",
                "data_date",
                "open_price",
                "close_price",
                "volume",
            ]
        )

        writer.writeheader()

        for record in records:
            writer.writerow(record)

    print()
    print(
        f"Market records generated: "
        f"{len(records)}"
    )

    print(
        f"Dataset saved to: "
        f"{OUTPUT_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("DemandIQ Market Data Generator")
    print("-" * 40)

    print(f"Start date: {START_DATE}")
    print(f"Days: {DAYS_TO_GENERATE}")

    connection = get_connection()

    try:

        stocks = fetch_stocks(connection)

        print(
            f"Stocks found: {len(stocks)}"
        )

        if not stocks:
            print(
                "ERROR: No stocks found "
                "in the database."
            )
            return

        records = generate_market_data(
            stocks
        )

        save_dataset(records)

        print()
        print(
            "Generation completed successfully."
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()