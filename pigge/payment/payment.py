"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template, request, redirect, url_for
from pigge.payment.transaction import *
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


def k2k(receiver_wallet, amount):
    """
    amount : Amount to be transferred
    receiver_wallet =  W XXXXXXXXX (Wallet ID of receiver)
    sender = kid currently in session (logged in)
    """
    y = "K" + receiver_wallet[1:]
    receiver = fetch_receiver(y)
    payment_confirmation = [receiver, receiver_wallet, amount, y]
    if payment_confirmation[0]:
        return payment_confirmation
    else:
        flash("Wrong kid ID entered. Please try again!")


def execute_transaction(transaction, r_wallet, s_wallet, amount):
    if transaction.check_dependencies():
        # 2FA ON
        s_wallet.sub_funds(amount)
        s_wallet.onHold(amount)
        return "Parent Verification Required!"
    else:
        # 2FA OFF
        s_wallet.sub_funds(amount)
        r_wallet.add_funds(amount)
        return "Payment Successful!"


@payment_bp.route("/pay-another-kid", methods=["GET", "POST"])
def kid_2_kid():
    if request.method == "GET":
        # Load the K2K page
        return render_template('payment/k2k.html')

    if request.method == "POST":
        # Send k2k data and load confirmation page
        receiver_wallet = request.form.get('receiver_wallet_id')
        amount = int(request.form.get('amount'))
        data = k2k(receiver_wallet, amount)
        return render_template("payment/confirmation.html", data=data)


@payment_bp.route("/payment/confirmation", methods=["GET", "POST"])
def confirmation():
    if request.method == "POST":
        # Send confirmation data and load final transaction status page
        if request.form.get("confirmation") == "yes":
            sender_wallet = session['id']
            x = "K" + sender_wallet[1:]
            amount = int(request.form.get("amount"))
            y = request.form.get("wallet")
            transaction = TheTransaction(x, y, amount, category="K2K")
            s_wallet = TheWallet(x)
            r_wallet = TheWallet(y)
            transaction_status = execute_transaction(
                transaction, r_wallet, s_wallet, amount)
            transaction.db_commit()
            return render_template("payment/transaction_status.html", transaction_status=transaction_status)
        else:
            return redirect(url_for("kdash.kid_dashboard"))
