from flask import Blueprint, render_template, request
import random

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            error = "جميع الحقول مطلوبة"

    return render_template("login.html")


@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/password-reset")
def password_reset():
    return render_template("password_reset.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"
