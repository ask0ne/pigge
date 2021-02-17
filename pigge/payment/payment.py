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


def k2k():
    """
    amount : Amount to be transferred
    receiver_wallet =  W XXXXXXXXX (Wallet ID of receiver)
    sender = kid currently in session (logged in)
    """
    receiver_wallet = request.form.get('receiver_wallet_id')
    amount = int(request.form.get('amount'))

    y = "K" + receiver_wallet[1:]
    receiver = fetch_receiver(y)
    payment_confirmation = [receiver, receiver_wallet, amount, y]
    if payment_confirmation[0]:
        return payment_confirmation
    else:
        flash("Wrong kid ID entered. Please try again!")


@payment_bp.route("/pay-another-kid", methods=["GET", "POST"])
def kid_2_kid():
    if request.method == "GET":
        return render_template('payment/k2k.html')

    if request.method == "POST":
        data = k2k()
        kid_2_kid.info = data
        print(data)
        return render_template("payment/confirmation.html", data=data)


@payment_bp.route("/payment/confirmation", methods=["GET", "POST"])
def confirmation():
    if request.method == "POST":
        if request.form.get("confirmation") == "yes":
            # db.session.commit()
            info = kid_2_kid.info
            sender_wallet = session['id']
            x = "K" + sender_wallet[1:]
            y = info[3]
            amount = info[2]
            transaction = TheTransaction(x, y, amount, category="K2K")
            s_wallet = TheWallet(sender_wallet)
            r_wallet = TheWallet(info[1])
            if transaction.check_dependencies():
                # 2FA ON
                s_wallet.sub_funds(amount)
                s_wallet.onHold(amount)
                data = "Parent Verification Required!"
            else:
                # 2FA OFF
                s_wallet.sub_funds(amount)
                r_wallet.add_funds(amount)
                data = "Payment Successful!"
            transaction.db_commit()
            return render_template("payment/transaction_status.html", transaction_status=data)
        else:
            # rollback function here I guess
            # db.session.rollback()
            return redirect(url_for("kdash.kid_dashboard"))


@payment_bp.route("/transactions", methods=["GET"])
def trasnaction_history():
    if session["id"]:
        transactions = TransactionLogs(session["id"])
        return render_template("payment/history.html", transactions=transactions.history)
    else:
        return redirect(url_for("auth_bp.login"))
