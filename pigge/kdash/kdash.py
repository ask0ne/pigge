"""Handles Kid Dashboard functionality"""
from flask import Blueprint, session, render_template
from pigge.kdash.session import TheKid
from pigge.payment.wallet import TheWallet

kdash_bp = Blueprint('kdash', __name__, template_folder='templates')


@kdash_bp.route("/kid-dashboard", methods=["GET"])
def kid_dashboard():
    """Kid's dashboard code here"""
    mail = session['user_email']
    user = TheKid(mail)
    wallet = TheWallet(user.user.kid_id)
    session['id'] = wallet.wallet.wallet_id
    return render_template("kdash/kids_dash.html", user=user.user, wallet=wallet)
