from functools import wraps

from flask import Blueprint, jsonify, render_template, request, session

from database import get_connection


auth_bp = Blueprint("auth", __name__)


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "status": "error",
                "message": "Authentication required"
            }), 401

        return view_function(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):

            if "user_id" not in session:
                return jsonify({
                    "status": "error",
                    "message": "Authentication required"
                }), 401

            if session.get("role") not in allowed_roles:
                return jsonify({
                    "status": "error",
                    "message": "Access denied"
                }), 403

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator


@auth_bp.route("/")
def home():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Username and password are required"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, password, full_name, role
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    user_id, stored_username, stored_password, full_name, role = user

    if password != stored_password:
        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    session.clear()

    session["user_id"] = user_id
    session["username"] = stored_username
    session["full_name"] = full_name
    session["role"] = role

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user_id,
            "username": stored_username,
            "full_name": full_name,
            "role": role
        }
    })


@auth_bp.route("/session")
@login_required
def current_session():

    return jsonify({
        "status": "success",
        "user": {
            "id": session.get("user_id"),
            "username": session.get("username"),
            "full_name": session.get("full_name"),
            "role": session.get("role")
        }
    })


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()

    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    })