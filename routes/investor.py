from flask import Blueprint, render_template, request, redirect, session
from database import get_connection

investor_bp = Blueprint("investor", __name__)


# --------------------------------
# View Stocks
# --------------------------------

@investor_bp.route("/stocks")
def stocks():
    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stock_id,
            company_name,
            symbol,
            sector,
            current_price
        FROM stocks
    """)

    stocks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "stocks.html",
        stocks=stocks
    )


# --------------------------------
# Buy Stock Page
# --------------------------------

@investor_bp.route("/buy")
def buy():

    if "user_id" not in session:
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stock_id,
            company_name,
            symbol,
            sector,
            current_price
        FROM stocks
    """)

    stocks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "buy_stock.html",
        stocks=stocks
    )


# --------------------------------
# Buy Stock
# --------------------------------

@investor_bp.route("/buy-stock", methods=["POST"])
def buy_stock():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    stock_id = request.form["stock_id"]
    quantity = int(request.form["quantity"])

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT current_price
        FROM stocks
        WHERE stock_id=%s
    """, (stock_id,))

    stock = cursor.fetchone()

    if stock is None:
        cursor.close()
        connection.close()
        return "Stock not found."

    price = stock[0]

    cursor.execute("""
        INSERT INTO portfolio
        (user_id, stock_id, quantity, buy_price)
        VALUES(%s, %s, %s, %s)
    """, (user_id, stock_id, quantity, price))

    cursor.execute("""
        INSERT INTO transactions
        (user_id, stock_id, transaction_type, quantity, price)
        VALUES(%s, %s, 'BUY', %s, %s)
    """, (user_id, stock_id, quantity, price))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/portfolio")
# --------------------------------
# Portfolio
# --------------------------------

@investor_bp.route("/portfolio")
def portfolio():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            stocks.company_name,
            stocks.symbol,
            portfolio.quantity,
            portfolio.buy_price,
            portfolio.portfolio_id

        FROM portfolio

        JOIN stocks

        ON portfolio.stock_id = stocks.stock_id

        WHERE portfolio.user_id=%s
    """, (user_id,))

    portfolio = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "portfolio.html",
        portfolio=portfolio
    )

# --------------------------------
# Sell Stock
# --------------------------------

@investor_bp.route("/sell-stock", methods=["POST"])
def sell_stock():
    @investor_bp.route("/sell-stock", methods=["POST"])
    def sell_stock():

     if "user_id" not in session:
        return redirect("/")

    portfolio_id = request.form["portfolio_id"]

    portfolio_id = request.form["portfolio_id"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stock_id,
            quantity,
            buy_price,
            user_id
        FROM portfolio
        WHERE portfolio_id=%s
    """, (portfolio_id,))

    stock = cursor.fetchone()

    stock_id = stock[0]
    quantity = stock[1]
    price = stock[2]
    user_id = stock[3]

    cursor.execute("""
        INSERT INTO transactions
        (user_id, stock_id, transaction_type, quantity, price)
        VALUES(%s,%s,'SELL',%s,%s)
    """, (user_id, stock_id, quantity, price))

    cursor.execute("""
        DELETE FROM portfolio
        WHERE portfolio_id=%s
    """, (portfolio_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/portfolio")


# --------------------------------
# Transactions
# --------------------------------

@investor_bp.route("/transactions")
def transactions():
    if "user_id" not in session:
     return redirect("/")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            transactions.transaction_id,
            stocks.company_name,
            transactions.transaction_type,
            transactions.quantity,
            transactions.price,
            transactions.transaction_date

        FROM transactions

        JOIN stocks

        ON transactions.stock_id = stocks.stock_id

        ORDER BY transactions.transaction_date DESC
    """)

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "transactions.html",
        transactions=transactions
    )