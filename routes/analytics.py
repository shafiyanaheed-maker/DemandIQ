import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from flask import Blueprint, render_template, jsonify

from database import get_connection

analytics_bp = Blueprint("analytics", __name__)


# --------------------------------
# Demand Forecast
# --------------------------------

@analytics_bp.route("/forecast")
def forecast():

    connection = get_connection()

    query = """
        SELECT quantity_sold
        FROM sales
        ORDER BY sale_id
    """

    df = pd.read_sql(query, connection)

    connection.close()

    if len(df) == 0:

        prediction = 0
        quantities = []

    elif len(df) == 1:

        prediction = int(df["quantity_sold"].iloc[0])
        quantities = df["quantity_sold"].tolist()

    else:

        X = [[i] for i in range(len(df))]
        y = df["quantity_sold"]

        model = LinearRegression()
        model.fit(X, y)

        prediction = round(model.predict([[len(df)]])[0])
        quantities = y.tolist()

    graph_data = quantities + [prediction]

    plt.figure(figsize=(8,4))
    plt.plot(graph_data, marker="o")
    plt.title("Demand Forecast")
    plt.xlabel("Sales Record")
    plt.ylabel("Quantity Sold")
    plt.grid(True)

    folder = os.path.join("static", "graphs")

    if not os.path.exists(folder):
        os.makedirs(folder)

    plt.savefig(os.path.join(folder, "forecast.png"))
    plt.close()

    return render_template(
        "forecast.html",
        prediction=prediction
    )


# --------------------------------
# Total Products API
# --------------------------------

@analytics_bp.route("/api/total-products")
def total_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return jsonify({
    "total_products": total
})


# --------------------------------
# Total Revenue API
# --------------------------------

@analytics_bp.route("/api/total-revenue")
def total_revenue():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT IFNULL(SUM(revenue),0)
        FROM sales
    """)

    revenue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return jsonify({
    "total_revenue": revenue
})


# --------------------------------
# Total Stocks API
# --------------------------------

@analytics_bp.route("/api/total-stocks")
def total_stocks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM stocks
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return jsonify({
    "total_stocks": total
})


# --------------------------------
# Total Investors API
# --------------------------------

@analytics_bp.route("/api/total-investors")
def total_investors():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='Investor'
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    return jsonify({
    "total_investors": total
})