"""Handles Kid Dashboard functionality"""
from flask import Blueprint, session, render_template
from pigge.kdash.session import TheKid
from pigge.payment.wallet import TheWallet
from pigge.payment.logs import TransactionLogs

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
