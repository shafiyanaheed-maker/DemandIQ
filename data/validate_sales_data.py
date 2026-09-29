
import csv
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
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


def fetch_product_ids():
    """Get valid product IDs from the existing database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT product_id FROM products")
    product_ids = {row[0] for row in cursor.fetchall()}

    cursor.close()
    connection.close()

    return product_ids


def fetch_product_prices():
    """Get selling prices for all existing products."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT product_id, selling_price FROM products"
    )

    prices = {
        row[0]: Decimal(str(row[1]))
        for row in cursor.fetchall()
    }

    cursor.close()
    connection.close()

    return prices


# ============================================================
# VALIDATION
# ============================================================

def validate_file_exists():
    if not DATASET_FILE.exists():
        print(f"ERROR: Dataset not found: {DATASET_FILE}")
        return False

    return True


def validate_columns(rows):
    """Check that all required columns exist."""
    required_columns = {
        "product_id",
        "sale_date",
        "quantity_sold",
        "revenue",
    }

    if not rows:
        print("ERROR: Dataset contains no records.")
        return False

    actual_columns = set(rows[0].keys())

    missing = required_columns - actual_columns

    if missing:
        print(f"ERROR: Missing columns: {sorted(missing)}")
        return False

    return True


def validate_records(rows, valid_product_ids, product_prices):
    """Validate individual sales records."""

    errors = []

    for row_number, row in enumerate(rows, start=2):

        # ----------------------------------------------------
        # Product ID
        # ----------------------------------------------------

        try:
            product_id = int(row["product_id"])
        except (ValueError, TypeError):
            errors.append(
                f"Row {row_number}: invalid product_id"
            )
            continue

        if product_id not in valid_product_ids:
            errors.append(
                f"Row {row_number}: product_id {product_id} "
                f"does not exist"
            )

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        try:
            sale_date = date.fromisoformat(row["sale_date"])
        except (ValueError, TypeError):
            errors.append(
                f"Row {row_number}: invalid sale_date"
            )
            continue

        # ----------------------------------------------------
        # Quantity
        # ----------------------------------------------------

        try:
            quantity = int(row["quantity_sold"])
        except (ValueError, TypeError):
            errors.append(
                f"Row {row_number}: invalid quantity_sold"
            )
            continue

        if quantity <= 0:
            errors.append(
                f"Row {row_number}: quantity_sold must be greater than 0"
            )

        # ----------------------------------------------------
        # Revenue
        # ----------------------------------------------------

        try:
            revenue = Decimal(row["revenue"])
        except (InvalidOperation, ValueError, TypeError):
            errors.append(
                f"Row {row_number}: invalid revenue"
            )
            continue

        if revenue <= 0:
            errors.append(
                f"Row {row_number}: revenue must be greater than 0"
            )

        # ----------------------------------------------------
        # Revenue consistency
        # ----------------------------------------------------

        if product_id in product_prices:
            expected_revenue = (
                product_prices[product_id] * quantity
            ).quantize(Decimal("0.01"))

            actual_revenue = revenue.quantize(Decimal("0.01"))

            if actual_revenue != expected_revenue:
                errors.append(
                    f"Row {row_number}: revenue mismatch "
                    f"(expected {expected_revenue}, "
                    f"got {actual_revenue})"
                )

    return errors


def validate_duplicates(rows):
    """Check for duplicate product/date combinations."""

    combinations = [
        (
            row["product_id"],
            row["sale_date"],
        )
        for row in rows
    ]

    counts = Counter(combinations)

    duplicates = [
        item for item, count in counts.items()
        if count > 1
    ]

    return duplicates


def validate_product_coverage(rows, valid_product_ids):
    """Check whether every product has generated sales."""

    dataset_products = {
        int(row["product_id"])
        for row in rows
    }

    missing_products = valid_product_ids - dataset_products

    return missing_products


# ============================================================
# MAIN VALIDATION
# ============================================================

def main():

    print("DemandIQ Sales Dataset Validator")
    print("=" * 40)

    # --------------------------------------------------------
    # File check
    # --------------------------------------------------------

    if not validate_file_exists():
        return

    # --------------------------------------------------------
    # Load CSV
    # --------------------------------------------------------

    with open(
        DATASET_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    print(f"Records loaded: {len(rows)}")

    if not validate_columns(rows):
        return

    # --------------------------------------------------------
    # Database reference data
    # --------------------------------------------------------

    valid_product_ids = fetch_product_ids()
    product_prices = fetch_product_prices()

    print(f"Products in database: {len(valid_product_ids)}")

    # --------------------------------------------------------
    # Record validation
    # --------------------------------------------------------

    errors = validate_records(
        rows,
        valid_product_ids,
        product_prices,
    )

    # --------------------------------------------------------
    # Duplicate validation
    # --------------------------------------------------------

    duplicates = validate_duplicates(rows)

    # --------------------------------------------------------
    # Product coverage
    # --------------------------------------------------------

    missing_products = validate_product_coverage(
        rows,
        valid_product_ids,
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print()
    print("VALIDATION RESULTS")
    print("-" * 40)

    if errors:
        print(f"❌ Record errors: {len(errors)}")

        for error in errors[:10]:
            print(f"   {error}")

        if len(errors) > 10:
            print(
                f"   ... and {len(errors) - 10} more"
            )

    else:
        print("✅ Record validation passed")

    if duplicates:
        print(
            f"❌ Duplicate product/date combinations: "
            f"{len(duplicates)}"
        )
    else:
        print("✅ No duplicate product/date combinations")

    if missing_products:
        print(
            f"❌ Products without sales data: "
            f"{len(missing_products)}"
        )
        print(
            f"   Product IDs: "
            f"{sorted(missing_products)}"
        )
    else:
        print("✅ All database products have sales data")

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    if not errors and not duplicates and not missing_products:
        print()
        print("🎉 DATASET VALIDATION PASSED")
        print("The dataset is ready for database seeding.")

    else:
        print()
        print("⚠️ DATASET VALIDATION FAILED")
        print("Fix the reported issues before seeding MySQL.")


if __name__ == "__main__":
    main()

