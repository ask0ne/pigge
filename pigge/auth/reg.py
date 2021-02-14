"""
Contains functions that access the database such as login and registration.
"""

from pigge.auth.extras import *
from pigge.models import db, Parent, Kid, Wallet, RequestFunds
from datetime import datetime


def calculate_id(name, dob):
    """Generate ID in form of Uddnnyy00x"""
    generated_id = 'K'
    dd = str(dob[-2:])
    nn = str(cal_name(name[0]))
    yy = str(dob[2:4])
    auto_inc_id = db.engine.execute('select count(id) from kid').scalar() + 1
    auto_inc_id = str("{0:0=3d}".format(auto_inc_id))
    generated_id += dd + nn + yy + auto_inc_id
    return generated_id


def check_unique_user(mobile, email):
    """Returns True if user is unique"""
    mail = Parent.query.filter_by(parent_email=email).first()
    phno = Parent.query.filter_by(phone_number=mobile).first()
    if mail or phno:
        return False
    return True


def createParent(pname, mobile, email, password):
    """Create new parent entry in database"""
    p_user = Parent(created_on=datetime.now(), parent_name=pname, phone_number=mobile,
                    parent_email=email, parent_password=password, acc_status=-1)
    db.session.add(p_user)
    db.session.commit()


def createKid(kid_id, name, birthdate, email, pin, gender):
    """Create new kid entry in database"""
    k_user = Kid(kid_id=kid_id, kid_name=name, kid_dob=birthdate,
                 kid_email=email, kid_pin=pin, kid_gender=gender, number_of_tries=0)
    db.session.add(k_user)


def createWallet(kid_id):
    """Create new wallet entry in database"""
    wallet_ID = "W" + kid_id[1:]
    wallet = Wallet(wallet_id=wallet_ID, balance=0, generated_on=datetime.now(), pay_request=False,
                    two_f_auth=-1, restrict_bal=0, on_hold=0)
    db.session.add(wallet)
    something = RequestFunds(wallet_id=wallet_ID, amount=0, message=None)
    db.session.add(something)
    db.session.commit()


def updateParent(parent_mail, kid_id):
    """Update parent ID according to the kid ID"""
    p_user = Parent.query.filter_by(parent_email=parent_mail).first()
    p_user.acc_status = 1
    p_user.parent_id = "P" + kid_id[1:]
    db.session.commit()


def authenticateParent(parent_mail, ppassword):
    """Parent login authentication"""
    user = Parent.query.filter_by(parent_email=parent_mail).first()
    password_hash = user.parent_password
    status = user.acc_status
    # Incorrect email or password
    if not (user and verify_password(ppassword, password_hash)):
        return -1

    # Check account status to check if kid account exists or not
    if status != -1:
        return 1
    else:
        return 0


def authenticateKid(kmail, kpin):
    """Kid login authentication"""
    user = Kid.query.filter_by(kid_email=kmail).first()
    pin = user.kid_pin
    auth = 0
    if not user:
        # Incorrect email
        auth = 0
    elif kpin != pin:
        # Incorrect pin
        if user.number_of_tries < 5:
            user.number_of_tries += 1
            auth = 0
        else:
            # Incorrect pin tries exceeded
            user.number_of_tries = 0
            auth = -1
    else:
        # Correct pin
        user.number_of_tries = 0
        auth = 1
    db.session.commit()
    return auth
