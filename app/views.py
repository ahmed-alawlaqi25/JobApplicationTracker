from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/job-tracker")
def job_tracker():
    return render_template("job_tracker.html")
