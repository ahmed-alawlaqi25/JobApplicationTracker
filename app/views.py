from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

views = Blueprint("views", __name__)
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))
admin_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))


@views.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("views.tracker"))

    return render_template("home.html")


@views.route("/tracker")
def tracker():
    user_id = session["user_id"]
    user_supabase = get_user_supabase()
    if not user_supabase:
        return redirect(url_for("auth.register"))
    job_info_response = user_supabase.table("job").select("*").eq("user_id", user_id).execute()
    jobs = job_info_response.data
    return render_template("tracker.html", jobs=jobs)


@views.route("/add-job", methods=["POST"])
def add_job():
    user_supabase = get_user_supabase()
    if not user_supabase:
        return redirect(url_for("auth.register"))

    job_url = request.form.get("job_url")
    job_title = request.form.get("job_title")
    company_name = request.form.get("company_name")
    city = request.form.get("city")
    date_of_publish = request.form.get("date_of_publish")
    job_description = request.form.get("job_description")
    job_status = request.form.get("job_status")
    notes = request.form.get("notes")
    user_id = session["user_id"]

    user_supabase.table("job").insert({
        "user_id": user_id,
        "job_url": job_url,
        "job_title": job_title,
        "company_name": company_name,
        "city": city,
        "published": date_of_publish,
        "job_description": job_description,
        "status": job_status,
        "user_note": notes
    }).execute()
    return redirect(url_for('views.tracker'))


def get_valid_token():
    try:
        refreshed = supabase.auth.refresh_session(session["refresh_token"])
        session["access_token"] = refreshed.session.access_token
        session["refresh_token"] = refreshed.session.refresh_token
        return session["access_token"]
    except Exception as e:
        print(e)
        session.clear()
        return None


def get_user_supabase():
    access_token = get_valid_token()
    if not access_token:
        return None
    user_supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))
    user_supabase.postgrest.auth(access_token)
    return user_supabase


@views.route("/application/<job_id>", methods=["GET"])
def application(job_id):
    user_supabase = get_user_supabase()
    if not user_supabase:
        return redirect(url_for("auth.register"))
    job_info_response = user_supabase.table("job").select("*").eq("job_id", job_id).execute()
    jobs = job_info_response.data

    return render_template("application.html", jobs=jobs)


@views.route("/switch_status", methods=["POST"])
def switch_status():
    try:
        data = request.get_json()
        job_id = data["job_id"]
        status = data["status"]
        user_supabase = get_user_supabase()
        if not user_supabase:
            return redirect(url_for("auth.register"))
        update_row = (
            supabase.table("job")
            .update({"status": status})
            .eq("job_id", job_id)
            .execute()
        )
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "error"}


@views.route("/delete_job", methods=["POST"])
def delete_job():
    try:
        data = request.get_json()
        job_id = data["job_id"]
        user_supabase = get_user_supabase()
        if not user_supabase:
            return redirect(url_for("auth.register"))
        delete_row = (
            user_supabase.table("job")
            .delete()
            .eq("job_id", job_id)
            .execute()
        )
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "error"}


@views.route("/resume_review")
def resume_review():
    return render_template("resume_review.html")


@views.route("/document")
def document():
    return render_template("document.html")


@views.route("/settings")
def settings():
    user_supabase = get_user_supabase()
    if not user_supabase:
        return redirect(url_for("auth.register"))
    user_data = supabase.auth.get_user()

    return render_template("settings.html", user_data=user_data)


@views.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.register"))

    user_supabase = get_user_supabase()
    if not user_supabase:
        return redirect(url_for("auth.register"))

    try:
        user_supabase.table("users").delete().eq("id", user_id).execute()
        admin_supabase.auth.admin.delete_user(user_id)  # service-role client
        session.clear()
        return redirect(url_for("auth.register"))
    except Exception as e:
        print(e)
        flash("حدث خطأ أثناء حذف الحساب، حاول مرة أخرى", "error")
        return redirect(url_for("views.settings"))


@views.route("/dashboard", )
def dashboard():
    return render_template("dashboard.html")
