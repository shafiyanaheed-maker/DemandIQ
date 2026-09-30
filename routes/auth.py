from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    jsonify,
)

from database import get_connection


auth_bp = Blueprint("auth", __name__)


def login_required(view_function):
    """
    Require the user to be logged in before accessing a route.
    """

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")

        return view_function(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    """
    Require the user to be logged in and have one of the allowed roles.
    """

    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/")

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
        return "Username and password are required", 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                password,
                full_name,
                role
            FROM users
            WHERE username=%s
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
        return "Invalid Username or Password", 401

    user_id = user[0]
    stored_username = user[1]
    stored_password = user[2]
    full_name = user[3]
    role = user[4]

    # Current database contains existing passwords.
    # Password hashing migration will be handled separately.
    if password != stored_password:
        return "Invalid Username or Password", 401

    # Prevent session fixation by clearing any previous session.
    session.clear()

    session["user_id"] = user_id
    session["username"] = stored_username
    session["full_name"] = full_name
    session["role"] = role

    if role == "Business":
        return redirect("/business")

    if role == "Investor":
        return redirect("/investor")

    if role == "Admin":
        return redirect("/admin-dashboard")

    session.clear()
    return "Invalid user role", 403


@auth_bp.route("/business")
@role_required("Business")
def business():
    return render_template("business_dashboard.html")


@auth_bp.route("/investor")
@role_required("Investor")
def investor():
    return render_template("investor_dashboard.html")


@auth_bp.route("/admin")
@role_required("Admin")
def admin():
    return render_template("admin_dashboard.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")