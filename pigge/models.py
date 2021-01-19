'''Models(Database) Code Here'''
from flask_sqlalchemy import SQLAlchemy

# Database DB configurations
db = SQLAlchemy()


class Parent(db.Model):
    '''Parent Personal Details'''
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime)
    parent_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    parent_email = db.Column(db.String)
    parent_password = db.Column(db.String)
    acc_status = db.Column(db.Boolean)


class Panel(db.Model):
    """Parent Panel : pay_request, two_f_auth and restrict_bal"""
    __tablename__ = 'panel'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String)
    pay_request = db.Column(db.Boolean)
    two_f_auth = db.Column(db.Boolean)
    restrict_bal = db.Column(db.Integer)


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
