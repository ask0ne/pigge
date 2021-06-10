from pigge.models import db, Wallet, Services


class TheWallet:
    def __init__(self, some_id):
        self.wallet = Wallet.query.filter_by(
            wallet_id=self.generate_wallet_id(some_id)).first()
        self.checkbox_2FA = self.check_2FA()
        self.checkbox_limit = self.check_rbalance()
        self.real_balance = self.wallet.balance + self.wallet.on_hold

    def generate_wallet_id(self, some_id):
        return 'W' + some_id[1:]

    def add_funds(self, val):
        self.wallet.balance += val
        self.wallet.restrict_bal += val
        db.session.commit()

    def sub_funds(self, val):
        if self.wallet.restrict_bal >= val:
            self.wallet.balance -= val
            self.wallet.restrict_bal -= val
        db.session.commit()

    def onHold(self, val):
        self.wallet.on_hold += val
        db.session.commit()

    def check_rbalance(self):
        if self.wallet.restrict_bal == self.wallet.balance:
            return None
        else:
            return "checked"

    def check_2FA(self):
        if self.wallet.two_f_auth == -1:
            return None
        else:
            return "checked"

    def spend_limit(self, val):
        if val < self.wallet.balance and val > 0:
            self.wallet.restrict_bal = val
        else:
            self.wallet.restrict_bal = self.wallet.balance
        db.session.commit()

    def change_2FA(self, val):
        self.wallet.two_f_auth = val
        db.session.commit()


class TheService:
    def __init__(self, category):
        # Category - Fun, Food, Travel, Stationary
        print(category)
        self.service = Services.query.filter_by(service_id=str(category)).first()
        print(self.service)

    def checkout(self, amount):
        self.service.balance += amount
