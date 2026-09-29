import csv
import random
from datetime import date, timedelta
from decimal import Decimal

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

OUTPUT_FILE = "data/sales_dataset.csv"

# Start with 7 days for testing.
# Change to 365 after validation succeeds.
DAYS_TO_GENERATE = 365

START_DATE = date.today() - timedelta(days=DAYS_TO_GENERATE - 1)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


# ============================================================
# DEMAND PROFILES
# ============================================================

# Base daily demand by sub-category.
# These are starting points, not final demand values.
DEMAND_PROFILES = {
    "Smartphones": (8, 22),
    "Laptops": (4, 12),
    "Gaming Laptops": (3, 10),
    "Tablets": (4, 11),
    "Headphones": (7, 20),
    "Gaming Headsets": (5, 15),
    "Accessories": (12, 35),
    "Smart Watches": (5, 15),
    "Wearables": (5, 14),
    "Televisions": (2, 8),
    "Monitors": (3, 9),
    "Speakers": (5, 15),
    "Cameras": (2, 7),
    "Camera Accessories": (4, 12),
    "Gaming Consoles": (2, 8),
    "Printers": (2, 7),
    "Home Appliances": (3, 10),
    "Clothing": (8, 25),
    "Shoes": (5, 16),
    "Bags": (4, 14),
    "Fashion Accessories": (6, 18),
}


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    """Create a connection to the DemandIQ MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def fetch_products():
    """Fetch the existing product catalog."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            product_id,
            sku,
            product_name,
            category,
            sub_category,
            selling_price
        FROM products
        ORDER BY product_id
    """

    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


# ============================================================
# DEMAND CALCULATION
# ============================================================

def get_base_demand(sub_category):
    """Return a random base demand for the product."""
    low, high = DEMAND_PROFILES.get(sub_category, (4, 12))
    return random.randint(low, high)


def get_weekday_factor(current_date):
    """
    Apply weekday/weekend demand behavior.

    Saturday and Sunday generally have higher consumer demand.
    """
    weekday = current_date.weekday()

    if weekday == 5:       # Saturday
        return 1.20
    if weekday == 6:       # Sunday
        return 1.15

    return 1.00


def get_seasonal_factor(current_date, category, sub_category):
    """
    Add simple seasonal behavior.

    The project can later replace this with a more advanced
    seasonality model.
    """
    month = current_date.month

    factor = 1.0

    # Festival/holiday shopping period.
    if month in (10, 11):
        factor *= 1.25

    # Back-to-school / education-related demand.
    if month in (6, 7):
        if sub_category in {
            "Laptops",
            "Gaming Laptops",
            "Tablets",
            "Printers",
            "Accessories",
        }:
            factor *= 1.15

    # Summer demand.
    if month in (4, 5):
        if sub_category in {
            "Home Appliances",
            "Televisions",
            "Speakers",
        }:
            factor *= 1.10

    # Fashion seasonality.
    if category == "Fashion":
        if month in (10, 11, 12):
            factor *= 1.15

    return factor


def get_product_factor(product_id):
    """
    Give each product a stable demand multiplier.

    This prevents all products in the same category from
    behaving identically.
    """
    random.seed(RANDOM_SEED + product_id)

    factor = random.uniform(0.75, 1.30)

    # Restore the global random seed used by the generator.
    random.seed(RANDOM_SEED)

    return factor


def calculate_quantity(product, current_date, base_demand):
    """Calculate realistic daily quantity sold."""
    category = product["category"]
    sub_category = product["sub_category"]
    product_id = product["product_id"]

    weekday_factor = get_weekday_factor(current_date)
    seasonal_factor = get_seasonal_factor(
        current_date,
        category,
        sub_category,
    )
    product_factor = get_product_factor(product_id)

    random_variation = random.uniform(0.85, 1.15)

    quantity = (
        base_demand
        * weekday_factor
        * seasonal_factor
        * product_factor
        * random_variation
    )

    return max(1, round(quantity))


# ============================================================
# DATA GENERATION
# ============================================================

def generate_sales_data(products):
    """Generate synthetic historical sales records."""
    records = []

    # Give every product its own stable base demand.
    product_base_demand = {
        product["product_id"]: get_base_demand(product["sub_category"])
        for product in products
    }

    for product in products:
        product_id = product["product_id"]
        selling_price = Decimal(str(product["selling_price"]))

        for day_offset in range(DAYS_TO_GENERATE):
            current_date = START_DATE + timedelta(days=day_offset)

            quantity_sold = calculate_quantity(
                product,
                current_date,
                product_base_demand[product_id],
            )

            revenue = Decimal(quantity_sold) * selling_price

            records.append({
                "product_id": product_id,
                "sale_date": current_date.isoformat(),
                "quantity_sold": quantity_sold,
                "revenue": round(revenue, 2),
            })

    return records


# ============================================================
# CSV OUTPUT
# ============================================================

def save_to_csv(records):
    """Save generated sales data to CSV."""
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "product_id",
                "sale_date",
                "quantity_sold",
                "revenue",
            ],
        )

        writer.writeheader()
        writer.writerows(records)


# ============================================================
# MAIN
# ============================================================

def main():
    print("DemandIQ Sales Dataset Generator")
    print("-" * 40)

    products = fetch_products()

    if not products:
        print("ERROR: No products found in the database.")
        return

    print(f"Products found: {len(products)}")
    print(f"Start date: {START_DATE}")
    print(f"Days: {DAYS_TO_GENERATE}")

    records = generate_sales_data(products)

    save_to_csv(records)

    print(f"Sales records generated: {len(records)}")
    print(f"Dataset saved to: {OUTPUT_FILE}")
    print("Generation completed successfully.")


if __name__ == "__main__":
    main()