import random
from datetime import datetime
from pigge.models import Transaction, Wallet, Kid, db

def fetch_receiver(k_id):
        receiver = Kid.query.filter_by(kid_id=k_id).first()
        if receiver:
            return receiver.kid_name
        else:
            return False
        
class TheTransaction:
    def __init__(self, x, y, amount, category):
        self.sender = x
        self.receiver = y
        self.amount = amount
        self.category = category
        self.payment_status = 1

        # Do something here, depending on type of transaction
        # Create a branched condition here for P2K, K2K and K2B
    def check_dependencies(self):
        """
        Check payment category.
        Check 2FA(if enabled) -- return True/False
        """
        if self.category == "K2K":
            wall_id = "W" + self.sender[1:]
            check_TFA = Wallet.query.filter_by(wallet_id=wall_id).first()
            if check_TFA.two_f_auth == 0 or check_TFA.two_f_auth < self.amount:
                self.payment_status = -1
                check_TFA.pay_request = True
                return True
            else:
                self.payment_status = 1
                return False


    def db_commit(self):
        """Final stage of transaction"""
        transaction = Transaction(transaction_id=self.generate_transaction_id(), timestamp=datetime.now(),
                                  sender_id=self.sender, receiver_id=self.receiver, amount=self.amount, category=self.category, status=self.payment_status)
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

    
