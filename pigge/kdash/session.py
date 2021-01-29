"""Handling kid sessions"""
from pigge.models import db, Kid, Wallet


class TheKid:
    """Initialize parent on login"""

    def __init__(self, mail):
        self.user = Kid.query.filter_by(kid_email=mail).first()
        self.wallet = Wallet.query.filter_by(
            wallet_id=generate_wallet_id(self.user)).first()

    def pay_kid(self, val):
        pass

    def request_funds(self, val):
        pass

    def pay_service(self, val):
        pass

    def view_transactions(self):
        pass

    def generate_wallet_id(self, user):
        wid = 'W' + user.kid_id[1:]
        return wid

    def check_user(self, wid):
        if Wallet.query.filter_by(wallet_id=wid).first():
            return True
        return False

    def check_amount(self, val):
        if val > self.wallet.restrict_bal and self.wallet.restrict_bal > 0:
            return True
        return False

    def execute_transaction(self, receiver, val):
        # Check for failures if any
        receiver = Wallet.query.filter_by(wallet_id=receiver).first()
        self.wallet.balance = self.wallet.balance - val
        receiver.balance = receiver.balance + val
        