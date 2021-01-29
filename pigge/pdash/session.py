"""Handling parent sessions"""
from pigge.models import db, Parent, Wallet


class TheParent:
    """Initialize parent on login"""

    def __init__(self, mail):
        # List of attributes to be displayed on dashboard
        self.user = Parent.query.filter_by(parent_email=mail).first()
        self.wallet = Wallet.query.filter_by(wallet_id=calculate_wallet_id(self)).first()
        self.two_fac_auth = check_two_factor(self)
        self.wallet_status = check_user_status(self)

    def calculate_wallet_id(self):
        return 'W' + self.user.parent_id[1:]

    def check_two_factor(self):
        if self.wallet.two_f_auth == -1:
            return None
        else:
            return "checked"

    def check_user_status(self):
        if self.user.acc_status == 0:
            return "checked"
        else:
            return None

    def add_funds(self, val):
        # Send into transactions
        self.wallet.balance += val
        db.session.commit()

    def two_f_auth(self, val):
        self.wallet.two_f_auth = val
        db.session.commit()

    def spend_limit(self, val):
        if val < self.wallet.balance and val > 0:
            self.wallet.restrict_bal = val
        else:
            self.wallet.restrict_bal = self.wallet.balance
        db.session.commit()

    def change_wallet(self, val):
        self.user.acc_status = val
        db.session.commit()
