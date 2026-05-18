from flask import Blueprint, render_template, request, redirect, url_for, session
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")

        password = request.form.get("password")
        password2 = request.form.get("password2")
        if password != password2:
            error_password = "Passwords must match."
            return render_template("register.html", error_password=error_password)

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        print(email, password, first_name, last_name)
        return redirect(url_for("views.job_tracker"))
    else:
        return render_template("register.html")


@auth.route("/signin", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        sign_in_data = request.form
        email = sign_in_data.get("email")
        try:
            supabase.auth.sign_in_with_otp({"email": email})
        except Exception as e:
            error_message = "Something went wrong, please try again."
            return render_template("sign_in.html", error_message=error_message)

        return redirect(url_for("auth.confirmemail"))
    else:
        return render_template("sign_in.html")


@auth.route("/confirmemail")
def confirmemail():
    return render_template("confirmemail.html")


@auth.route("/callback")
def callback():
    return render_template("callback.html")
