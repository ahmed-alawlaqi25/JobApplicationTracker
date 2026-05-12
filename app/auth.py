from flask import Blueprint, render_template, request
import re

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        register_data = request.form

        fname = register_data.get("fname", "")
        fname_length = len(fname)
        if fname_length < 2:
            print("Error name too short")

        lname = register_data.get("lname", "")
        lname_length = len(lname)
        if lname_length < 2:
            print("Error last name too short")

        email = register_data.get("email", "")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            print("Error: Invalid email format")
        else:
            print("Email is valid!")

        password = register_data.get("password", "")
        password_length = len(password)
        if password_length < 7:
            print("Error with password")

        print(email, password, fname, lname)

    else:
        return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_data = request.form
    email = login_data.get("email")
    password = login_data.get("password")
    print(email, password)

    return render_template("login.html")


@auth.route("/password-reset", methods=["GET", "POST"])
def password_reset():
    return render_template("password_reset.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"
