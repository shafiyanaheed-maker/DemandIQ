import csv
from datetime import datetime
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

EXPECTED_STOCKS = 5
EXPECTED_DAYS = 365
EXPECTED_RECORDS = EXPECTED_STOCKS * EXPECTED_DAYS


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_valid_stock_ids(connection):
    """Return stock IDs that exist in the database."""

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


# ============================================================
# DATASET VALIDATION
# ============================================================

def load_dataset():
    """Load the generated market dataset."""

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


def validate_records(records, valid_stock_ids):

    errors = []

    required_columns = {
        "stock_id",
        "data_date",
        "open_price",
        "close_price",
        "volume",
    }

    if not records:
        errors.append("Dataset is empty.")
        return errors

    # --------------------------------------------------------
    # Column validation
    # --------------------------------------------------------

    actual_columns = set(records[0].keys())

    missing_columns = (
        required_columns - actual_columns
    )

    if missing_columns:
        errors.append(
            "Missing columns: "
            + ", ".join(missing_columns)
        )

        return errors

    # --------------------------------------------------------
    # Record validation
    # --------------------------------------------------------

    seen_combinations = set()

    for index, row in enumerate(records, start=2):

        try:
            stock_id = int(row["stock_id"])

            open_price = float(
                row["open_price"]
            )

            close_price = float(
                row["close_price"]
            )

            volume = int(
                row["volume"]
            )

            data_date = datetime.strptime(
                row["data_date"],
                "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError) as error:

            errors.append(
                f"Row {index}: invalid value - {error}"
            )

            continue

        # Stock relationship
        if stock_id not in valid_stock_ids:

            errors.append(
                f"Row {index}: stock_id "
                f"{stock_id} does not exist."
            )

        # Date
        if data_date is None:

            errors.append(
                f"Row {index}: invalid date."
            )

        # Prices
        if open_price <= 0:

            errors.append(
                f"Row {index}: open price "
                f"must be greater than 0."
            )

        if close_price <= 0:

            errors.append(
                f"Row {index}: close price "
                f"must be greater than 0."
            )

        # Volume
        if volume <= 0:

            errors.append(
                f"Row {index}: volume "
                f"must be greater than 0."
            )

        # Duplicate stock/date
        combination = (
            stock_id,
            data_date
        )

        if combination in seen_combinations:

            errors.append(
                f"Row {index}: duplicate "
                f"stock/date combination "
                f"{combination}."
            )

        seen_combinations.add(combination)

    return errors


def validate_coverage(records, valid_stock_ids):

    errors = []

    # --------------------------------------------------------
    # Number of records
    # --------------------------------------------------------

    if len(records) != EXPECTED_RECORDS:

        errors.append(
            f"Expected {EXPECTED_RECORDS} records "
            f"but found {len(records)}."
        )

    # --------------------------------------------------------
    # Stock coverage
    # --------------------------------------------------------

    dataset_stock_ids = {
        int(row["stock_id"])
        for row in records
    }

    missing_stocks = (
        valid_stock_ids - dataset_stock_ids
    )

    if missing_stocks:

        errors.append(
            "Stocks without market data: "
            + ", ".join(
                map(str, sorted(missing_stocks))
            )
        )

    # --------------------------------------------------------
    # Date coverage
    # --------------------------------------------------------

    dates = [
        datetime.strptime(
            row["data_date"],
            "%Y-%m-%d"
        ).date()
        for row in records
    ]

    if dates:

        first_date = min(dates)
        last_date = max(dates)

        actual_days = (
            last_date - first_date
        ).days + 1

        if actual_days != EXPECTED_DAYS:

            errors.append(
                f"Expected {EXPECTED_DAYS} days "
                f"but found {actual_days} days."
            )

    return errors


# ============================================================
# MAIN
# ============================================================

def main():

    print("DemandIQ Market Data Validator")
    print("=" * 45)

    connection = get_connection()

    try:

        # ----------------------------------------------------
        # Load dataset
        # ----------------------------------------------------

        records = load_dataset()

        print(
            f"Records loaded: {len(records)}"
        )

        # ----------------------------------------------------
        # Fetch stocks
        # ----------------------------------------------------

        valid_stock_ids = (
            fetch_valid_stock_ids(connection)
        )

        print(
            f"Stocks in database: "
            f"{len(valid_stock_ids)}"
        )

        # ----------------------------------------------------
        # Validate records
        # ----------------------------------------------------

        record_errors = validate_records(
            records,
            valid_stock_ids
        )

        coverage_errors = validate_coverage(
            records,
            valid_stock_ids
        )

        all_errors = (
            record_errors
            + coverage_errors
        )

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        print()
        print("VALIDATION RESULTS")
        print("-" * 45)

        if not record_errors:

            print(
                "✅ Record validation passed"
            )

        else:

            print(
                f"❌ Record validation failed "
                f"({len(record_errors)} errors)"
            )

        if not any(
            "duplicate" in error.lower()
            for error in record_errors
        ):

            print(
                "✅ No duplicate stock/date combinations"
            )

        else:

            print(
                "❌ Duplicate stock/date combinations found"
            )

        if not coverage_errors:

            print(
                "✅ Stock and date coverage passed"
            )

        else:

            print(
                "❌ Stock/date coverage failed"
            )

        # ----------------------------------------------------
        # Detailed errors
        # ----------------------------------------------------

        if all_errors:

            print()
            print("ERROR DETAILS")
            print("-" * 45)

            for error in all_errors[:20]:

                print(f"❌ {error}")

            if len(all_errors) > 20:

                print()
                print(
                    f"... and "
                    f"{len(all_errors) - 20} more errors."
                )

            print()
            print(
                "⚠️ DATASET VALIDATION FAILED"
            )

        else:

            print()
            print(
                "🎉 MARKET DATASET VALIDATION PASSED"
            )

            print(
                "The market dataset is ready "
                "for database seeding."
            )

    finally:

        connection.close()


if __name__ == "__main__":
    main()