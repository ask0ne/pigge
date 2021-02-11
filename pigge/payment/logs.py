from pigge.models import db, Transaction
from pigge.payment.wallet import TheWallet


class TransactionLogs:
    def __init__(self, wallet_id):
        self.k_id = "K" + wallet_id[1:]
        self.history = Transaction.query.filter_by(sender_id=self.k_id).all()
        #self.history = Transaction.query.join(Kid, Transaction.receiver_id==Kid.kid_id).filter_by(sender_id=self.k_id).all()
        #self.history = Transaction.query.join(Kid, Transaction.receiver_id==Kid.kid_id).add_columns(bla bla,Kid.kid_name).filter_by(sender_id=self.k_id).all()


class PayRequests:
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id
        self.k_id = "K" + wallet_id[1:]
        self.history = Transaction.query.filter_by(sender_id=self.k_id, status=-1).all()

    def accept_request(self, tr_id):
        transaction = Transaction.query.filter_by(transaction_id=tr_id).first()
        transaction.status = 1
        sender_wallet = TheWallet(self.wallet_id)
        sender_wallet.wallet.on_hold -= transaction.amount
        receiver_wallet_id = "W" + transaction.receiver_id[1:]
        receiver_wallet = TheWallet(receiver_wallet_id)
        receiver_wallet.add_funds(transaction.amount)
        db.session.commit()

    def reject_request(self, tr_id):
        transaction = Transaction.query.filter_by(transaction_id=tr_id).first()
        transaction.status = 0
        sender_wallet = TheWallet(self.wallet_id)
        sender_wallet.wallet.on_hold -= transaction.amount
        sender_wallet.add_funds(transaction.amount)
        db.session.commit()
