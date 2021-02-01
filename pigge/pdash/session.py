"""Handling parent sessions"""
from pigge.models import db, Parent, Wallet


class TheParent:
    """Initialize parent on login"""

    def __init__(self, mail):
        # List of attributes to be displayed on dashboard
        self.user = Parent.query.filter_by(parent_email=mail).first()
        self.wallet_status = self.check_user_status()

    def check_user_status(self):
        if self.user.acc_status == 0:
            return "checked"
        else:
            return None

    def change_wallet(self, val):
        self.user.acc_status = val
        db.session.commit()
