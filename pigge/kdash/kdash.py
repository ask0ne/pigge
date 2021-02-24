"""Handles Kid Dashboard functionality"""
from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from pigge.kdash.session import TheKid
from pigge.payment.wallet import TheWallet
from pigge.payment.logs import TransactionLogs, RequestFunds

kdash_bp = Blueprint('kdash', __name__, template_folder='templates')


@kdash_bp.route("/kid-dashboard", methods=["GET"])
def kid_dashboard():
    """Kid's dashboard code here"""
    mail = session['user_email']
    user = TheKid(mail)
    wallet = TheWallet(user.user.kid_id)
    session['id'] = wallet.wallet.wallet_id
    return render_template("kdash/kids_dash.html", user=user.user, wallet=wallet)


@kdash_bp.route("/transactions", methods=["GET"])
def trasnaction_history():
    if session["id"]:
        transactions = TransactionLogs(session["id"])
        return render_template("payment/history.html", transactions=transactions.history)
    else:
        return redirect(url_for("auth_bp.login"))


@kdash_bp.route("/requesting_funds", methods=["POST"])
def request_funds():
    amount = int(request.form.get('amount'))
    message = request.form.get('message')
    print(amount, message)
    new_request = RequestFunds(session['id'])
    print(amount, message)
    if new_request.is_unique():
        new_request.create(amount, message)
        new_request.execute_request()
        flash("Fund request successful!")
    else:
        flash("Request already pending!")
    return redirect(url_for("kdash.kid_dashboard"))
