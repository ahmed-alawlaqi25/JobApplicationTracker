from flask import Blueprint, render_template, request, redirect, url_for, session

views = Blueprint("views", __name__)


@views.route("/")
def base():
    if "user" in session:
        return redirect(url_for("views.tracker"))

    return render_template("home.html")


@views.route("/tracker")
def job_tracker():
    return render_template("tracker.html")
