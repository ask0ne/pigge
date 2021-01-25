"""Handling parent sessions"""
from pigge.models import db, Parent, Wallet


class TheParent:
    """Initialize parent on login"""

    def __init__(self, mail):
        self.user = Parent.query.filter_by(parent_email=mail).first()
        wallet_id = 'W' + self.user.parent_id[1:]
        self.wallet = Wallet.query.filter_by(wallet_id = wallet_id).first()

    def add_funds(self, val):
        self.wallet.balance += val
        db.session.commit()