from pigge import main
from pigge.models import db, Transaction, Kid, FundRequests, Services
from pigge.payment.wallet import TheWallet
from sqlalchemy import join, func


class TransactionLogs:
    def __init__(self, wallet_id):
        self.k_id = "K" + wallet_id[1:]

        k2k_history = db.session.query(Kid, Transaction).filter(Transaction.receiver_id == Kid.kid_id).filter(Transaction.sender_id == self.k_id).all()
        history_k2k = db.session.query(Kid, Transaction).filter(Transaction.sender_id == Kid.kid_id).filter(Transaction.receiver_id == self.k_id).filter(Transaction.status == 1).all()
        k2b_history = db.session.query(Services, Transaction).filter(Transaction.receiver_id == Services.service_id).filter(Transaction.sender_id == self.k_id).all()
        self.history = k2k_history + history_k2k + k2b_history
        # For pie chart
        k2k = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.sender_id == self.k_id).filter(Transaction.category == "K2K").all()
        food = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.sender_id == self.k_id).filter(Transaction.receiver_id == "S202102").all()
        fun = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.sender_id == self.k_id).filter(Transaction.receiver_id == "S202101").all()
        travel = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.sender_id == self.k_id).filter(Transaction.receiver_id == "S202104").all()
        stationary = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.sender_id == self.k_id).filter(Transaction.receiver_id == "S202103").all()
        self.pie = []
        self.pie.append(k2k.pop()[0])
        self.pie.append(stationary.pop()[0])
        self.pie.append(food.pop()[0])
        self.pie.append(travel.pop()[0])
        self.pie.append(fun.pop()[0])
        for i in range(5):
            if self.pie[i] is None:
                self.pie[i] = 0


class ParentLogs:
    def __init__(self, wallet_id):
        self.p_id = "P" + wallet_id[1:]
        self.history = db.session.query(Transaction).filter_by(sender_id=self.p_id).all()
        print(self.p_id, self.history)
        for transaction in self.history:
            print(transaction.amount)
            print(transaction.transaction_id)

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
