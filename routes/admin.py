from flask import Blueprint, render_template, session, redirect
from database import get_connection

admin_bp = Blueprint("admin", __name__)
def admin_required():
    if "user_id" not in session:
        return False

    return session.get("role") == "Admin"


# --------------------------------
# Admin Dashboard
# --------------------------------

@admin_bp.route("/admin-dashboard")
def admin_dashboard():
    if not admin_required():
     return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Total Products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Total Sales
    cursor.execute("SELECT COUNT(*) FROM sales")
    total_sales = cursor.fetchone()[0]

    # Total Stocks
    cursor.execute("SELECT COUNT(*) FROM stocks")
    total_stocks = cursor.fetchone()[0]

    # Total Revenue
    cursor.execute("""
        SELECT IFNULL(SUM(revenue),0)
        FROM sales
    """)
    total_revenue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_products=total_products,
        total_sales=total_sales,
        total_stocks=total_stocks,
        total_revenue=total_revenue
    )


# --------------------------------
# Users List
# --------------------------------

@admin_bp.route("/users")
def users():
    if not admin_required():
     return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            email,
            role
        FROM users
    """)

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "users.html",
        users=users
    )


# --------------------------------
# Products Report
# --------------------------------

@admin_bp.route("/admin-products")
def admin_products():
    if not admin_required():
     return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM products
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products_list.html",
        products=products
    )


# --------------------------------
# Sales Report
# --------------------------------

@admin_bp.route("/admin-sales")
def admin_sales():
    if not admin_required():
     return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            sales.sale_id,
            products.product_name,
            sales.sale_date,
            sales.quantity_sold,
            sales.revenue

        FROM sales

        JOIN products

        ON sales.product_id = products.product_id

    """)

    sales = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "sales_list.html",
        sales=sales
    )


# --------------------------------
# Stocks Report
# --------------------------------

@admin_bp.route("/admin-stocks")
def admin_stocks():
    if not admin_required():
     return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM stocks
    """)

    stocks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "stocks.html",
        stocks=stocks
    )