"""Handles Parent Dashboard functionality"""
from flask import Blueprint, session, render_template, request, redirect, url_for
import random
from datetime import datetime
from pigge.kdash.session import TheKid
from pigge.payment.transaction import Transaction

payment_bp = Blueprint('payment', __name__, template_folder='templates')

@payment_bp.route("/pay-user", methods=["GET"])
def kid_2_kid():
    return render_template(url_for('payment/kid-to-kid.html'))


@payment_bp.route("/pay-user-inprogress", methods=["POST"])
def k2k():
    reciever_wallet = request.form.get('kid_id')
    reciever = 'K' + reciever_wallet[1:]
    amount = request.form.get('amount')
    sender = generate_sender(session['user_email'])
    sender_id = sender.kid_id
    transaction_id = generate_transaction_id()
    verify_transaction(receiver, sender, amount)

def p2k():
    


def generate_transaction_id():
    """
    rrrDDMMrrr
    """
    dd = str(datetime.now().day)
    mm = str(datetime.now().month)
    transaction_id = str(random.randint(10**3, 10**4-1)) + dd + mm + str(random.randint(10**3, 10**4-1))
    return int(transaction_id)


def generate_sender(mail):
    user = TheKid(user)
    return user

def generate_transaction(sender, receiver, amount):
    sender.execute_transaction(receiver, amount)
    t_id = generate_transaction_id()
    sender.user.kid_id

def verify_transaction(receiver, sender, amount):
    
    if sender.check_user(receiver):
        if sender.check_amount(amount):
            generate_transaction(sender, receiver, amount)
        else:
            # Error for amount
    else:
        # Error for wrong receiver ID