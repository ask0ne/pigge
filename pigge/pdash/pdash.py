"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template, request, redirect, url_for
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
    val = int(request.form.get("add_funds"))
    user = TheParent(session['user_email'])
    user.add_funds(val)
    return redirect(url_for('pdash.parent_dashboard'))


@pdash_bp.route("/parent-dashboard", methods=["POST"])
def max_spend_limit():
    """Limit max spending amount (min) balance"""
    val = int(request.form.get("min_balance"))
    user = TheParent(session['user_email'])
    return redirect(url_for("pdash.parent_dashboard"))


def two_fac_auth():
    pass


def wallet_status():
    pass
