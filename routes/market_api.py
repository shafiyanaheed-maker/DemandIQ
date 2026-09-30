from functools import wraps

from flask import Blueprint, jsonify, request, session

from database import get_connection


market_api_bp = Blueprint(
    "market_api",
    __name__,
    url_prefix="/api/market"
)


def investor_or_admin_required(view_function):
    """Allow only logged-in Investor or Admin users."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "status": "error",
                "message": "Authentication required"
            }), 401

        if session.get("role") not in ("Investor", "Admin"):
            return jsonify({
                "status": "error",
                "message": "Access denied"
            }), 403

        return view_function(*args, **kwargs)

    return wrapped_view


@market_api_bp.route("/stocks", methods=["GET"])
@investor_or_admin_required
def get_stocks():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                stock_id,
                company_name,
                symbol,
                sector,
                current_price,
                created_at
            FROM stocks
            ORDER BY company_name
        """)

        stocks = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(stocks),
            "stocks": stocks
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve stocks",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route("/stocks/<int:stock_id>", methods=["GET"])
@investor_or_admin_required
def get_stock(stock_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                stock_id,
                company_name,
                symbol,
                sector,
                current_price,
                created_at
            FROM stocks
            WHERE stock_id = %s
        """, (stock_id,))

        stock = cursor.fetchone()

        if not stock:
            return jsonify({
                "status": "error",
                "message": "Stock not found"
            }), 404

        return jsonify({
            "status": "success",
            "stock": stock
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve stock",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route(
    "/stocks/<int:stock_id>/history",
    methods=["GET"]
)
@investor_or_admin_required
def get_stock_history(stock_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                stock_id,
                data_date,
                open_price,
                close_price,
                volume
            FROM market_data
            WHERE stock_id = %s
            ORDER BY data_date ASC
        """, (stock_id,))

        history = cursor.fetchall()

        if not history:
            return jsonify({
                "status": "error",
                "message": "No market history found"
            }), 404

        return jsonify({
            "status": "success",
            "stock_id": stock_id,
            "count": len(history),
            "history": history
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve market history",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route(
    "/stocks/<int:stock_id>/latest",
    methods=["GET"]
)
@investor_or_admin_required
def get_latest_market_data(stock_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                stock_id,
                data_date,
                open_price,
                close_price,
                volume
            FROM market_data
            WHERE stock_id = %s
            ORDER BY data_date DESC
            LIMIT 1
        """, (stock_id,))

        latest = cursor.fetchone()

        if not latest:
            return jsonify({
                "status": "error",
                "message": "Market data not found"
            }), 404

        return jsonify({
            "status": "success",
            "market_data": latest
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve latest market data",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route("/portfolio", methods=["GET"])
@investor_or_admin_required
def get_portfolio():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        user_id = session["user_id"]

        cursor.execute("""
            SELECT
                p.portfolio_id,
                p.user_id,
                p.stock_id,
                s.company_name,
                s.symbol,
                s.sector,
                p.quantity,
                p.buy_price,
                s.current_price,
                (
                    p.quantity * s.current_price
                ) AS current_value,
                (
                    p.quantity *
                    (s.current_price - p.buy_price)
                ) AS unrealized_profit_loss
            FROM portfolio p
            INNER JOIN stocks s
                ON p.stock_id = s.stock_id
            WHERE p.user_id = %s
            ORDER BY s.company_name
        """, (user_id,))

        portfolio = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(portfolio),
            "portfolio": portfolio
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve portfolio",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route("/transactions", methods=["GET"])
@investor_or_admin_required
def get_transactions():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        user_id = session["user_id"]

        cursor.execute("""
            SELECT
                t.transaction_id,
                t.user_id,
                t.stock_id,
                s.company_name,
                s.symbol,
                t.transaction_type,
                t.quantity,
                t.price,
                t.transaction_date
            FROM transactions t
            INNER JOIN stocks s
                ON t.stock_id = s.stock_id
            WHERE t.user_id = %s
            ORDER BY t.transaction_date DESC,
                     t.transaction_id DESC
        """, (user_id,))

        transactions = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(transactions),
            "transactions": transactions
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve transactions",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route("/buy", methods=["POST"])
@investor_or_admin_required
def buy_stock():
    """Buy shares at the stock's current price."""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON request body is required"
        }), 400

    try:
        stock_id = int(data["stock_id"])
        quantity = int(data["quantity"])
    except (KeyError, TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "stock_id and quantity must be integers"
        }), 400

    if stock_id <= 0 or quantity <= 0:
        return jsonify({
            "status": "error",
            "message": "stock_id and quantity must be greater than zero"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                stock_id,
                company_name,
                symbol,
                current_price
            FROM stocks
            WHERE stock_id = %s
            FOR UPDATE
        """, (stock_id,))

        stock = cursor.fetchone()

        if not stock:
            connection.rollback()

            return jsonify({
                "status": "error",
                "message": "Stock not found"
            }), 404

        user_id = session["user_id"]
        price = float(stock["current_price"])

        cursor.execute("""
            SELECT
                portfolio_id,
                quantity,
                buy_price
            FROM portfolio
            WHERE user_id = %s
              AND stock_id = %s
            FOR UPDATE
        """, (user_id, stock_id))

        holding = cursor.fetchone()

        if holding:
            old_quantity = int(holding["quantity"])
            old_buy_price = float(holding["buy_price"])

            new_quantity = old_quantity + quantity

            weighted_price = (
                (old_quantity * old_buy_price)
                + (quantity * price)
            ) / new_quantity

            cursor.execute("""
                UPDATE portfolio
                SET
                    quantity = %s,
                    buy_price = %s
                WHERE portfolio_id = %s
            """, (
                new_quantity,
                weighted_price,
                holding["portfolio_id"]
            ))

        else:
            cursor.execute("""
                INSERT INTO portfolio (
                    user_id,
                    stock_id,
                    quantity,
                    buy_price
                )
                VALUES (%s, %s, %s, %s)
            """, (
                user_id,
                stock_id,
                quantity,
                price
            ))

        cursor.execute("""
            INSERT INTO transactions (
                user_id,
                stock_id,
                transaction_type,
                quantity,
                price
            )
            VALUES (%s, %s, 'BUY', %s, %s)
        """, (
            user_id,
            stock_id,
            quantity,
            price
        ))

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Stock purchased successfully",
            "transaction": {
                "stock_id": stock_id,
                "symbol": stock["symbol"],
                "quantity": quantity,
                "price": price,
                "total_value": round(
                    quantity * price,
                    2
                )
            }
        }), 201

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "status": "error",
            "message": "Failed to complete purchase",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@market_api_bp.route("/sell", methods=["POST"])
@investor_or_admin_required
def sell_stock():
    """Sell shares owned by the logged-in investor."""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON request body is required"
        }), 400

    try:
        stock_id = int(data["stock_id"])
        quantity = int(data["quantity"])
    except (KeyError, TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "stock_id and quantity must be integers"
        }), 400

    if stock_id <= 0 or quantity <= 0:
        return jsonify({
            "status": "error",
            "message": "stock_id and quantity must be greater than zero"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        user_id = session["user_id"]

        cursor.execute("""
            SELECT
                p.portfolio_id,
                p.quantity,
                p.buy_price,
                s.symbol,
                s.current_price
            FROM portfolio p
            INNER JOIN stocks s
                ON p.stock_id = s.stock_id
            WHERE p.user_id = %s
              AND p.stock_id = %s
            FOR UPDATE
        """, (user_id, stock_id))

        holding = cursor.fetchone()

        if not holding:
            connection.rollback()

            return jsonify({
                "status": "error",
                "message": "No holding found for this stock"
            }), 404

        owned_quantity = int(holding["quantity"])

        if quantity > owned_quantity:
            connection.rollback()

            return jsonify({
                "status": "error",
                "message": "Insufficient shares",
                "owned_quantity": owned_quantity,
                "requested_quantity": quantity
            }), 409

        price = float(holding["current_price"])

        remaining_quantity = owned_quantity - quantity

        if remaining_quantity == 0:
            cursor.execute("""
                DELETE FROM portfolio
                WHERE portfolio_id = %s
            """, (holding["portfolio_id"],))

        else:
            cursor.execute("""
                UPDATE portfolio
                SET quantity = %s
                WHERE portfolio_id = %s
            """, (
                remaining_quantity,
                holding["portfolio_id"]
            ))

        cursor.execute("""
            INSERT INTO transactions (
                user_id,
                stock_id,
                transaction_type,
                quantity,
                price
            )
            VALUES (%s, %s, 'SELL', %s, %s)
        """, (
            user_id,
            stock_id,
            quantity,
            price
        ))

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Stock sold successfully",
            "transaction": {
                "stock_id": stock_id,
                "symbol": holding["symbol"],
                "quantity": quantity,
                "price": price,
                "total_value": round(
                    quantity * price,
                    2
                ),
                "remaining_quantity": remaining_quantity
            }
        }), 201

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "status": "error",
            "message": "Failed to complete sale",
            "details": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()