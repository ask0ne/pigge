"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template
from pigge.pdash.session import TheParent

pdash_bp = Blueprint('pdash', __name__, template_folder='templates')


@pdash_bp.route("/parent-dashboard", methods=["GET", "POST"])
def parent_dashboard():
    """Parent's dashboard code here"""
    mail = session['user_email']
    user = TheParent(mail)
    return render_template("pdash/parent_dashboard.html", user=user.user)
