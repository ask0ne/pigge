"""Handles Parent Dashboard functionality"""
from pigge.payment import transaction
from flask import Blueprint, session, render_template, request, redirect, url_for
from pigge.pdash.session import TheParent
from pigge.payment.wallet import TheWallet
from pigge.payment.payment import p2k
from pigge.payment.logs import PayRequests, ParentLogs, RequestFunds, TransactionLogs

pdash_bp = Blueprint('pdash', __name__, template_folder='templates')


@pdash_bp.route("/parent-dashboard", methods=["GET"])
def parent_dashboard():
    """Parent's dashboard code here"""
    user = TheParent(session['user_email'])
    wallet = TheWallet(user.user.parent_id)
    session['id'] = wallet.wallet.wallet_id
    logs = PayRequests(session['id'])
    frequest = RequestFunds(session['id'])
    return render_template("pdash/parent_dashboard.html", user=user, wallet=wallet, logs=logs, frequest=frequest)


@pdash_bp.route("/parent-dashboard-add-funds", methods=["POST"])
def add_funds():
    """Add funds endpoint"""
    val = int(request.form.get("add_funds"))
    p2k(val)
    return redirect(url_for('pdash.parent_dashboard'))


@pdash_bp.route("/parent-dashboard-max-spend-limit", methods=["POST"])
def max_spend_limit():
    """Limit max spending amount (min) balance"""
    if request.form.get("check_box") == None:
        val = 0
    else:
        val = int(request.form.get("min_balance"))
    wallet = TheWallet(session['id'])
    wallet.spend_limit(val)
    return redirect(url_for("pdash.parent_dashboard"))


@pdash_bp.route("/parent-dashboard-2FA", methods=["POST"])
def two_factor_authentication():
    if request.form.get("check_box") == None:
        val = -1
    else:
        val = request.form.get("two_f_a")
    wallet = TheWallet(session['id'])
    wallet.change_2FA(int(val))
    return redirect(url_for('pdash.parent_dashboard'))


@pdash_bp.route("/parent-dashboard-wallet", methods=["POST"])
def wallet_status():
    if request.form.get("wallet_status") == None:
        val = 1  # True aka wallet is active
    else:
        val = 0  # False
    user = TheParent(session['user_email'])
    user.change_wallet(int(val))
    return redirect(url_for('pdash.parent_dashboard'))


@pdash_bp.route("/parent-dashboard-2FA-authenticate", methods=["POST"])
def request_handling():
    pay = PayRequests(session['id'])
    tr_id = request.form.get("transaction_id")
    if request.form.get("req_button") == "yes":
        pay.accept_request(tr_id)
    elif request.form.get("req_button") == "no":
        pay.reject_request(tr_id)
    return redirect(url_for("pdash.parent_dashboard"))


@pdash_bp.route("/parent_transactions", methods=["GET"])
def view_transactions():
    if session["id"]:
        logs = ParentLogs(session['id'])
        return render_template("payment/parent_history.html", logs=logs.history)
    else:
        return redirect(url_for("auth_bp.login"))


@pdash_bp.route("/fund_request", methods=["POST"])
def request_funds():
    frequest = RequestFunds(session['id'])
    if request.form.get("submit") == "yes":
        p2k(frequest.get_amount())
    frequest.delete()
    return redirect(url_for("pdash.parent_dashboard"))
