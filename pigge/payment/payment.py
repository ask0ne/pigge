"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template, request, redirect, url_for
from pigge.kdash.session import TheKid
from pigge.payment.transaction import TheTransaction
from pigge.payment.wallet import TheWallet
from pigge.payment.logs import TransactionLogs

payment_bp = Blueprint('payment', __name__, template_folder='templates')


def p2k(amount):
    """
    val : Amount to be added
    user : Wallet ID (Kid)
    """
    category = "P2K"
    wallet_id = session['id']
    x = "P" + wallet_id[1:]
    y = "K" + wallet_id[1:]
    transaction = TheTransaction(x, y, amount, category)
    wallet = TheWallet(wallet_id)
    wallet.add_funds(amount)
    transaction.db_commit()


def k2k():
    """
    amount : Amount to be transferred
    receiver_wallet =  W XXXXXXXXX (Wallet ID of receiver)
    sender = kid currently in session (logged in)
    """
    receiver_wallet = request.form.get('receiver_wallet_id')
    amount = int(request.form.get('amount'))
    sender_wallet = session['id']
    x = "K" + sender_wallet[1:]
    y = "K" + receiver_wallet[1:]
    transaction = TheTransaction(x, y, amount, category="K2K")
    s_wallet = TheWallet(sender_wallet)
    r_wallet = TheWallet(receiver_wallet)
    if transaction.verify_receiver(receiver_wallet):
        # s_wallet.sub_funds(amount)
        # r_wallet.add_funds(amount)
        data = transaction.check_dependencies()
        if data == "Payment Successful":
            s_wallet.sub_funds(amount)
            r_wallet.add_funds(amount)
        else:
            s_wallet.sub_funds(amount)
            s_wallet.onHold(amount)
            
        transaction.db_commit()
        return data

    else:
        flash("Wrong kid ID entered. Please try again!")


@payment_bp.route("/transaction-status", methods=["GET"])
def transaction_status():
    return render_template("payment/transaction_status.html", transaction_status=request.args.get('data'))


@payment_bp.route("/pay-another-kid", methods=["GET", "POST"])
def kid_2_kid():
    if request.method == "GET":
        return render_template('payment/k2k.html')

    if request.method == "POST":
        data = k2k()
        return redirect(url_for("payment.transaction_status", data=data))


@payment_bp.route("/transactions", methods=["GET"])
def trasnaction_history():
    if session["id"]:
        transactions = TransactionLogs(session["id"])
        return render_template("payment/history.html", transactions=transactions.history)
    else:
        return redirect(url_for("auth_bp.login"))