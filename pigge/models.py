'''Models(Database) Code Here'''
from flask_sqlalchemy import SQLAlchemy
# Database DB configurations
db = SQLAlchemy()


class Parent(db.Model):
    '''Parent Personal Details'''
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    parent_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    parent_email = db.Column(db.String)
    parent_password = db.Column(db.LargeBinary)
    acc_status = db.Column(db.Integer)


class Wallet(db.Model):
    """Wallet"""
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.String)
    balance = db.Column(db.Integer)
    generated_on = db.Column(db.DateTime)
    pay_request = db.Column(db.Boolean)
    two_f_auth = db.Column(db.Integer)
    restrict_bal = db.Column(db.Integer)
    on_hold = db.Column(db.Integer)


class Kid(db.Model):
    """Kid Personal Details"""
    __tablename__ = 'kid'
    id = db.Column(db.Integer, primary_key=True)
    kid_id = db.Column(db.String)
    kid_name = db.Column(db.String)
    kid_dob = db.Column(db.String)
    kid_gender = db.Column(db.String)
    kid_email = db.Column(db.String)
    kid_pin = db.Column(db.String)
    number_of_tries = db.Column(db.Integer)


class Transaction(db.Model):
    """
    Status --
        -1: Pending
        0 : Rejected
        1 : Completed
    """
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String)
    timestamp = db.Column(db.String)
    sender_id = db.Column(db.String)
    receiver_id = db.Column(db.String)
    amount = db.Column(db.Integer)
    category = db.Column(db.String)
    status = db.Column(db.Integer)


class Services(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String)
    service_id = db.Column(db.String)
    balance = db.Column(db.Integer)

class FundRequests(db.Model):
    __tablename__ = "requestfunds"
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.String)
    amount = db.Column(db.Integer)
    message = db.Column(db.String)