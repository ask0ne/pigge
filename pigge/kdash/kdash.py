"""Handles Kid Dashboard functionality"""
from flask import Blueprint, session, render_template
from pigge.kdash.session import TheKid

kdash_bp = Blueprint('kdash', __name__, template_folder='templates')


@kdash_bp.route("/kid-dashboard", methods=["GET", "POST"])
def kid_dashboard():
    """Kid's dashboard code here"""
    mail = session['user_email']
    user = TheKid(mail)
    return render_template("kdash/kids_dash.html", user=user.user)
