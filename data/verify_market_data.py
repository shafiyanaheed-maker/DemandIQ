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

EXPECTED_RECORDS = 1825
EXPECTED_STOCKS = 5
EXPECTED_DAYS = 365


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# VERIFICATION
# ============================================================

def main():

    print("DemandIQ Market Data Verification")
    print("=" * 50)

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Total records
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM market_data"
    )

    total_records = cursor.fetchone()[0]

    print(
        f"Total market records : {total_records}"
    )

    # --------------------------------------------------------
    # Distinct stocks
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(DISTINCT stock_id)
        FROM market_data
        """
    )

    total_stocks = cursor.fetchone()[0]

    print(
        f"Stocks with data     : {total_stocks}"
    )

    # --------------------------------------------------------
    # Date range
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            MIN(data_date),
            MAX(data_date)
        FROM market_data
        """
    )

    first_date, last_date = cursor.fetchone()

    print(
        f"First market date    : {first_date}"
    )

    print(
        f"Last market date     : {last_date}"
    )

    # --------------------------------------------------------
    # Number of days
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(DISTINCT data_date)
        FROM market_data
        """
    )

    total_days = cursor.fetchone()[0]

    print(
        f"Trading dates        : {total_days}"
    )

    # --------------------------------------------------------
    # Average closing price
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT ROUND(AVG(close_price), 2)
        FROM market_data
        """
    )

    average_close = cursor.fetchone()[0]

    print(
        f"Average close price  : {average_close}"
    )

    # --------------------------------------------------------
    # Total volume
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT SUM(volume)
        FROM market_data
        """
    )

    total_volume = cursor.fetchone()[0]

    print(
        f"Total trading volume : {total_volume}"
    )

    # --------------------------------------------------------
    # Duplicate stock/date combinations
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            stock_id,
            data_date,
            COUNT(*)
        FROM market_data
        GROUP BY
            stock_id,
            data_date
        HAVING COUNT(*) > 1
        """
    )

    duplicates = cursor.fetchall()

    print(
        f"Duplicate records    : {len(duplicates)}"
    )

    # --------------------------------------------------------
    # Invalid open prices
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM market_data
        WHERE open_price <= 0
        """
    )

    invalid_open = cursor.fetchone()[0]

    print(
        f"Invalid open prices  : {invalid_open}"
    )

    # --------------------------------------------------------
    # Invalid close prices
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM market_data
        WHERE close_price <= 0
        """
    )

    invalid_close = cursor.fetchone()[0]

    print(
        f"Invalid close prices : {invalid_close}"
    )

    # --------------------------------------------------------
    # Invalid volume
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM market_data
        WHERE volume <= 0
        """
    )

    invalid_volume = cursor.fetchone()[0]

    print(
        f"Invalid volume       : {invalid_volume}"
    )

    # --------------------------------------------------------
    # Stock relationship check
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(DISTINCT m.stock_id)
        FROM market_data m
        INNER JOIN stocks s
            ON m.stock_id = s.stock_id
        """
    )

    linked_stocks = cursor.fetchone()[0]

    print(
        f"Linked stocks        : {linked_stocks}"
    )

    # --------------------------------------------------------
    # Expected records
    # --------------------------------------------------------

    expected_records_check = (
        total_records == EXPECTED_RECORDS
    )

    expected_stocks_check = (
        total_stocks == EXPECTED_STOCKS
    )

    expected_days_check = (
        total_days == EXPECTED_DAYS
    )

    duplicate_check = (
        len(duplicates) == 0
    )

    price_check = (
        invalid_open == 0
        and invalid_close == 0
    )

    volume_check = (
        invalid_volume == 0
    )

    relationship_check = (
        linked_stocks == EXPECTED_STOCKS
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print()
    print("=" * 50)

    if (
        expected_records_check
        and expected_stocks_check
        and expected_days_check
        and duplicate_check
        and price_check
        and volume_check
        and relationship_check
    ):

        print(
            "🎉 MARKET DATABASE VERIFICATION PASSED"
        )

        print()
        print(
            "Market dataset is correctly populated "
            "and ready for trading analytics."
        )

    else:

        print(
            "⚠️ MARKET DATABASE VERIFICATION "
            "NEEDS ATTENTION"
        )

        print()
        print("Expected:")
        print(
            f"  Records : {EXPECTED_RECORDS}"
        )
        print(
            f"  Stocks  : {EXPECTED_STOCKS}"
        )
        print(
            f"  Days    : {EXPECTED_DAYS}"
        )

        print()
        print("Actual:")
        print(
            f"  Records : {total_records}"
        )
        print(
            f"  Stocks  : {total_stocks}"
        )
        print(
            f"  Days    : {total_days}"
        )

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()