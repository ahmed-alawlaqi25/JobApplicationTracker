from flask import Blueprint

auth = Blueprint("auth",__name__)

# @auth.route("login")
# def login():
#     return "Yo"
#
@auth.route("/login")
def login():
    return "<h1>login</h1>"

@auth.route("/register")
def register():
    return "<p>register</p>"

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

