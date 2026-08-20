from flask import Blueprint, render_template, request, redirect, session
from database import get_connection

business_bp = Blueprint("business", __name__)


# ---------------------------------------
# Business Dashboard
# ---------------------------------------

@business_bp.route("/business")
def business_dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template("business_dashboard.html")


# ---------------------------------------
# Products Page
# ---------------------------------------

@business_bp.route("/products")
def products():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT supplier_id, supplier_name
        FROM suppliers
        ORDER BY supplier_name
    """)

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        suppliers=suppliers
    )


# ---------------------------------------
# Add Product
# ---------------------------------------

@business_bp.route("/add-product", methods=["POST"])
def add_product():

    if "user_id" not in session:
        return redirect("/")

    sku = request.form["sku"]
    product_name = request.form["product_name"]
    brand = request.form["brand"]
    category = request.form["category"]
    sub_category = request.form["sub_category"]
    description = request.form["description"]
    supplier_id = request.form["supplier_id"]
    cost_price = request.form["cost_price"]
    selling_price = request.form["selling_price"]
    stock_quantity = request.form["stock_quantity"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO products(

            sku,
            product_name,
            brand,
            category,
            sub_category,
            description,
            supplier_id,
            cost_price,
            selling_price,
            stock_quantity

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    """, (

        sku,
        product_name,
        brand,
        category,
        sub_category,
        description,
        supplier_id,
        cost_price,
        selling_price,
        stock_quantity

    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/products-list")


# ---------------------------------------
# Product List
# ---------------------------------------

@business_bp.route("/products-list")
def products_list():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            p.product_id,
            p.sku,
            p.product_name,
            p.brand,
            p.category,
            p.sub_category,
            s.supplier_name,
            p.cost_price,
            p.selling_price,
            p.stock_quantity

        FROM products p

        LEFT JOIN suppliers s

        ON p.supplier_id = s.supplier_id

        ORDER BY p.product_name

    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products_list.html",
        products=products
    )
# ---------------------------------------
# Inventory
# ---------------------------------------

@business_bp.route("/inventory")
def inventory():

    if "user_id" not in session:
        return redirect("/")

    search = request.args.get("search", "")
    branch = request.args.get("branch", "")
    category = request.args.get("category", "")

    connection = get_connection()
    cursor = connection.cursor()

    query = """

        SELECT

            i.inventory_id,
            p.product_name,
            p.brand,
            p.category,
            b.branch_name,
            i.stock_quantity,
            i.reorder_level

        FROM inventory i

        JOIN products p
        ON i.product_id = p.product_id

        JOIN branches b
        ON i.branch_id = b.branch_id

        WHERE 1=1

    """

    values = []

    if search:
        query += """
        AND
        (
            p.product_name LIKE %s
            OR
            p.brand LIKE %s
        )
        """
        values.extend([
            "%" + search + "%",
            "%" + search + "%"
        ])

    if branch:
        query += " AND b.branch_name=%s"
        values.append(branch)

    if category:
        query += " AND p.category=%s"
        values.append(category)

    query += " ORDER BY p.product_name"

    cursor.execute(query, tuple(values))

    inventory = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT branch_name
        FROM branches
        ORDER BY branch_name
    """)
    branches = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT category
        FROM products
        ORDER BY category
    """)
    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "inventory.html",
        inventory=inventory,
        branches=branches,
        categories=categories,
        search=search,
        selected_branch=branch,
        selected_category=category
    )


# ---------------------------------------
# Low Stock Products
# ---------------------------------------

@business_bp.route("/low-stock")
def low_stock():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            p.product_name,
            p.brand,
            b.branch_name,
            i.stock_quantity,
            i.reorder_level

        FROM inventory i

        JOIN products p

        ON i.product_id = p.product_id

        JOIN branches b

        ON i.branch_id = b.branch_id

        WHERE

        i.stock_quantity <= i.reorder_level

        ORDER BY

        i.stock_quantity ASC

    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "low_stock.html",
        products=products
    )


# ---------------------------------------
# Update Inventory Stock
# ---------------------------------------

@business_bp.route("/update-stock/<int:inventory_id>", methods=["POST"])
def update_stock(inventory_id):

    if "user_id" not in session:
        return redirect("/")

    new_stock = request.form["stock_quantity"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        UPDATE inventory

        SET

        stock_quantity=%s

        WHERE inventory_id=%s

    """, (new_stock, inventory_id))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/inventory")

# ---------------------------------------
# Sales Page
# ---------------------------------------

@business_bp.route("/sales")
def sales():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            product_id,
            product_name,
            brand,
            selling_price,
            stock_quantity

        FROM products

        ORDER BY product_name

    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "sales.html",
        products=products
    )


# ---------------------------------------
# Add Sale
# ---------------------------------------

@business_bp.route("/add-sale", methods=["POST"])
def add_sale():

    if "user_id" not in session:
        return redirect("/")

    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            selling_price,
            stock_quantity

        FROM products

        WHERE product_id=%s

    """, (product_id,))

    product = cursor.fetchone()

    if product is None:

        cursor.close()
        connection.close()

        return "Product not found."

    selling_price = product[0]
    stock = product[1]

    if quantity > stock:

        cursor.close()
        connection.close()

        return "Not enough stock."

    revenue = quantity * selling_price

    cursor.execute("""

        INSERT INTO sales

        (

            product_id,
            sale_date,
            quantity_sold,
            revenue

        )

        VALUES

        (

            %s,
            CURDATE(),
            %s,
            %s

        )

    """, (product_id, quantity, revenue))

    cursor.execute("""

        UPDATE products

        SET stock_quantity = stock_quantity - %s

        WHERE product_id=%s

    """, (quantity, product_id))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/sales-list")


# ---------------------------------------
# Sales List
# ---------------------------------------

@business_bp.route("/sales-list")
def sales_list():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            sales.sale_id,

            products.product_name,

            products.brand,

            sales.sale_date,

            sales.quantity_sold,

            sales.revenue

        FROM sales

        JOIN products

        ON sales.product_id = products.product_id

        ORDER BY sales.sale_date DESC

    """)

    sales = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(

        "sales_list.html",

        sales=sales

    )


# ---------------------------------------
# Sales Dashboard
# ---------------------------------------

@business_bp.route("/sales-dashboard")
def sales_dashboard():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM sales

    """)

    total_sales = cursor.fetchone()[0]

    cursor.execute("""

        SELECT IFNULL(SUM(revenue),0)

        FROM sales

    """)

    revenue = cursor.fetchone()[0]

    cursor.execute("""

        SELECT IFNULL(SUM(quantity_sold),0)

        FROM sales

    """)

    quantity = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(

        "sales_dashboard.html",

        total_sales=total_sales,

        total_revenue=revenue,

        total_quantity=quantity

    )
# ---------------------------------------
# Edit Product
# ---------------------------------------

@business_bp.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        sku = request.form["sku"]
        product_name = request.form["product_name"]
        brand = request.form["brand"]
        category = request.form["category"]
        sub_category = request.form["sub_category"]
        description = request.form["description"]
        supplier_id = request.form["supplier_id"]
        cost_price = request.form["cost_price"]
        selling_price = request.form["selling_price"]
        stock_quantity = request.form["stock_quantity"]

        cursor.execute("""

            UPDATE products

            SET

                sku=%s,
                product_name=%s,
                brand=%s,
                category=%s,
                sub_category=%s,
                description=%s,
                supplier_id=%s,
                cost_price=%s,
                selling_price=%s,
                stock_quantity=%s

            WHERE product_id=%s

        """, (

            sku,
            product_name,
            brand,
            category,
            sub_category,
            description,
            supplier_id,
            cost_price,
            selling_price,
            stock_quantity,
            product_id

        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/products-list")

    cursor.execute("""

        SELECT *

        FROM products

        WHERE product_id=%s

    """, (product_id,))

    product = cursor.fetchone()

    cursor.execute("""

        SELECT supplier_id, supplier_name

        FROM suppliers

        ORDER BY supplier_name

    """)

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "edit_product.html",
        product=product,
        suppliers=suppliers
    )


# ---------------------------------------
# Delete Product
# ---------------------------------------

@business_bp.route("/delete-product/<int:product_id>")
def delete_product(product_id):

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        DELETE FROM products

        WHERE product_id=%s

    """, (product_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/products-list")


# ---------------------------------------
# Product Details API
# ---------------------------------------

@business_bp.route("/api/product/<int:product_id>")
def product_api(product_id):

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *

        FROM products

        WHERE product_id=%s

    """, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return product


# ---------------------------------------
# Products API
# ---------------------------------------

@business_bp.route("/api/products")
def products_api():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *

        FROM products

        ORDER BY product_name

    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "products": products
    }
# ---------------------------------------
# Business Dashboard
# ---------------------------------------

@business_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    # Total Products
    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)
    total_products = cursor.fetchone()[0]

    # Total Inventory Items
    cursor.execute("""
        SELECT IFNULL(SUM(stock_quantity),0)
        FROM inventory
    """)
    total_inventory = cursor.fetchone()[0]

    # Total Suppliers
    cursor.execute("""
        SELECT COUNT(*)
        FROM suppliers
    """)
    total_suppliers = cursor.fetchone()[0]

    # Total Branches
    cursor.execute("""
        SELECT COUNT(*)
        FROM branches
    """)
    total_branches = cursor.fetchone()[0]

    # Total Sales
    cursor.execute("""
        SELECT COUNT(*)
        FROM sales
    """)
    total_sales = cursor.fetchone()[0]

    # Revenue
    cursor.execute("""
        SELECT IFNULL(SUM(revenue),0)
        FROM sales
    """)
    total_revenue = cursor.fetchone()[0]

    # Low Stock
    cursor.execute("""
        SELECT COUNT(*)
        FROM inventory
        WHERE stock_quantity <= reorder_level
    """)
    low_stock = cursor.fetchone()[0]

    # Inventory Value
    cursor.execute("""
        SELECT
            IFNULL(
                SUM(products.cost_price * inventory.stock_quantity),
                0
            )

        FROM inventory

        JOIN products

        ON inventory.product_id = products.product_id
    """)
    inventory_value = cursor.fetchone()[0]

    # Top Selling Products
    cursor.execute("""

        SELECT

            products.product_name,

            SUM(sales.quantity_sold) total

        FROM sales

        JOIN products

        ON sales.product_id=products.product_id

        GROUP BY products.product_name

        ORDER BY total DESC

        LIMIT 5

    """)

    top_products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(

        "business_dashboard.html",

        total_products=total_products,

        total_inventory=total_inventory,

        total_suppliers=total_suppliers,

        total_branches=total_branches,

        total_sales=total_sales,

        total_revenue=total_revenue,

        low_stock=low_stock,

        inventory_value=inventory_value,

        top_products=top_products

    )