"""Handling parent sessions"""
from pigge.models import db, Parent, Wallet


class TheParent:
    """Initialize parent on login"""

    def __init__(self, mail):
        self.user = Parent.query.filter_by(parent_email=mail).first()
        wallet_id = 'W' + self.user.parent_id[1:]
        self.wallet = Wallet.query.filter_by(wallet_id=wallet_id).first()
        if self.wallet.two_f_auth == -1:
            self.two_fac_auth = None
        else:
            self.two_fac_auth = "checked"
        if self.user.acc_status == 0:
            self.wallet_status = "checked"
        else:
            self.wallet_status = None
        

    def add_funds(self, val):
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
