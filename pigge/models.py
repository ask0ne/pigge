'''Models(Database) Code Here'''
from flask_sqlalchemy import SQLAlchemy

#Database DB configurations
db = SQLAlchemy()

class Parent(db.Model):
    '''Parent information table'''
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    parent_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    parent_email = db.Column(db.String)
    parent_password = db.Column(db.String)
    salt = db.Column(db.String)