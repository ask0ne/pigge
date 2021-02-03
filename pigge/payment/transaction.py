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
        transaction_id = str(random.randint(10**2, 10**3-1)) + \
            dd + mm + str(random.randint(10**2, 10**3-1))
        return str(transaction_id)

    def verify_receiver(self, wid):
        """Function to verify that RECEIVER ID is valid aka user exists"""
        if Wallet.query.filter_by(wallet_id=wid).first():
            return True
        return False
