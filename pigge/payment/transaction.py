import random
from datetime import datetime
from pigge.models import Transaction, Wallet, db


class TheTransaction:
    def __init__(self, x, y, amount, category):
        self.sender = x
        self.receiver = y
        self.amount = amount
        self.category = category

        # Do something here, depending on type of transaction
        # Create a branched condition here for P2K, K2K and K2B

    def db_commit(self):
        """Final stage of transaction"""
        if self.category == "P2K":
            payment_status = 1
        else:
            payment_status = -1
        transaction = Transaction(transaction_id=self.generate_transaction_id(), timestamp=datetime.now(),
                                  sender_id=self.sender, receiver_id=self.receiver, amount=self.amount, category=self.category, status=payment_status)
        db.session.add(transaction)
        db.session.commit()

    def generate_transaction_id(self):
        """
        Generate transaction ID to store into db
        rrrDDMMrrr
        """
        dd = int(datetime.now().day)
        mm = int(datetime.now().month)
        dd = str(dd).zfill(2)
        mm = str(mm).zfill(2)
        transaction_id = str(random.randint(10**2, 10**3-1)) + dd + mm + str(random.randint(10**2, 10**3-1))
        return str(transaction_id)

    def generate_transaction(self, sender, receiver, amount):
        """IDK why tf I put this here"""
        sender.execute_transaction(receiver, amount)
        t_id = generate_transaction_id()
        sender.user.kid_id

    def verify_transaction(self):
        """IDK why tf I put this here"""
        if self.check_user(receiver):
            if self.check_amount(amount):
                return True

    def check_user(self, wid):
        """Function to verify that RECEIVER ID is valid aka user exists"""
        if Wallet.query.filter_by(wallet_id=wid).first():
            return True
        return False

    def check_amount(self, val):
        """Function to verify that sender has sufficient amount I think"""
        if val > self.wallet.restrict_bal and self.wallet.restrict_bal > 0:
            return True
        return False

    def execute_transaction(self, receiver, val):
        """IDK why tf I put this here"""
        # Check for failures if any
        receiver = Wallet.query.filter_by(wallet_id=receiver).first()
        self.wallet.balance = self.wallet.balance - val
        receiver.balance = receiver.balance + val
