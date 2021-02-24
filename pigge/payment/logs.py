from pigge import main
from pigge.models import db, Transaction, Kid, FundRequests
from pigge.payment.wallet import TheWallet
from sqlalchemy import join


class TransactionLogs:
    def __init__(self, wallet_id):
        self.k_id = "K" + wallet_id[1:]
        # self.history = Transaction.query.filter_by(sender_id=self.k_id).all()
        self.history = db.session.query(Kid, Transaction).filter(
            Transaction.receiver_id == Kid.kid_id).filter(Transaction.sender_id == self.k_id).all()


class ParentLogs:
    def __init__(self, wallet_id):
        self.p_id = "P" + wallet_id[1:]
        self.history = Transaction.query.filter_by(sender_id=self.p_id).all()


class PayRequests:
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id
        self.k_id = "K" + wallet_id[1:]
        self.history = Transaction.query.filter_by(
            sender_id=self.k_id, status=-1).all()

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


class RequestFunds:
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id
        self.existing_request = FundRequests.query.filter_by(
            wallet_id=self.wallet_id).first()

    def create(self, amount, message):
        self.amount = amount
        self.message = message

    def is_unique(self):
        """Check if any existing request"""
        if self.existing_request:
            return False
        else:
            return True

    def execute_request(self):
        """Entry into db"""
        new_request = FundRequests(
            wallet_id=self.wallet_id, message=self.message, amount=self.amount)
        db.session.add(new_request)
        db.session.commit()

    def delete(self):
        db.session.delete(self.existing_request)
        db.session.commit()

    def get_amount(self):
        return self.existing_request.amount
