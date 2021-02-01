"""Handling kid sessions"""
from pigge.models import db, Kid, Wallet


class TheKid:
    """Initialize parent on login"""

    def __init__(self, mail):
        self.user = Kid.query.filter_by(kid_email=mail).first()


    def pay_kid(self, val):
        pass

    def request_funds(self, val):
        pass

    def pay_service(self, val):
        pass

    def view_transactions(self):
        pass

        