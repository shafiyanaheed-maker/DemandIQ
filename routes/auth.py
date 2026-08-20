from flask import Blueprint, render_template, request, redirect, session
from database import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username=%s
        AND password=%s
    """, (username, password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:

        session["user_id"] = user[0]
        session["username"] = user[1]
        session["role"] = user[4]

        if session["role"] == "Business":
            return redirect("/business")

        elif session["role"] == "Investor":
            return redirect("/investor")

        else:
            return redirect("/admin")

    return "Invalid Username or Password"


@auth_bp.route("/business")
def business():
    return render_template("business_dashboard.html")


@auth_bp.route("/investor")
def investor():
    return render_template("investor_dashboard.html")


@auth_bp.route("/admin")
def admin():
    return render_template("admin_dashboard.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")