from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/")
def base():
    return render_template("home.html")


@views.route("/job-tracker")
def job_tracker():
    return render_template("job_tracker.html")
