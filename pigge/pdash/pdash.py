"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template, request, redirect,url_for
from pigge.pdash.session import TheParent

pdash_bp = Blueprint('pdash', __name__, template_folder='templates')


@pdash_bp.route("/parent-dashboard", methods=["GET"])
def parent_dashboard():
    """Parent's dashboard code here"""
    user = TheParent(session['user_email'])
    return render_template("pdash/parent_dashboard.html", user=user)


@pdash_bp.route("/parent-dashboard", methods=["POST"])
def add_funds():
    """Add funds endpoint"""
    val = request.form.get("add_funds")
    print(type(val), val)
    val = int(val)
    user = TheParent(session['user_email'])
    user.add_funds(val)
    return redirect(url_for('pdash.parent_dashboard'))
