"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template, request, redirect, url_for
from pigge.pdash.session import TheParent

pdash_bp = Blueprint('pdash', __name__, template_folder='templates')


@pdash_bp.route("/parent-dashboard", methods=["GET"])
def parent_dashboard():
    """Parent's dashboard code here"""
    user = TheParent(session['user_email'])
    return render_template("pdash/parent_dashboard.html", user=user)


@pdash_bp.route("/parent-dashboard-add-funds", methods=["POST"])
def add_funds():
    """Add funds endpoint"""
    val = request.form.get("add_funds")
    user = TheParent(session['user_email'])
    user.add_funds(int(val))
    return redirect(url_for('pdash.parent_dashboard'))


@pdash_bp.route("/parent-dashboard-max-spend-limit", methods=["POST"])
def max_spend_limit():
    """Limit max spending amount (min) balance"""
    val = int(request.form.get("min_balance"))
    user = TheParent(session['user_email'])
    user.spend_limit(val)
    return redirect(url_for("pdash.parent_dashboard"))


@pdash_bp.route("/parent-dashboard-2FA", methods=["POST"])
def two_fac_auth():
    if request.form.get("check_box") == None:
        val = -1
    else:
        val = request.form.get("two_f_a")
    user = TheParent(session['user_email'])
    user.two_f_auth(int(val))
    return redirect(url_for('pdash.parent_dashboard'))


@pdash_bp.route("/parent-dashboard-wallet", methods=["POST"])
def wallet_status():
    if request.form.get("wallet_status") == None:
        val = 1 # True aka wallet is active
    else:
        val = 0 # False
    user = TheParent(session['user_email'])
    user.change_wallet(int(val))
    return redirect(url_for('pdash.parent_dashboard'))
