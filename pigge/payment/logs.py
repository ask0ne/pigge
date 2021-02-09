from pigge.models import Transaction

class TransactionLogs:
    def __init__(self, wallet_id):
        self.k_id = "K" + wallet_id[1:] 
        self.history = Transaction.query.filter_by(sender_id=self.k_id).all()