'''Logic for auth module including login & ID verification'''
import os
import cv2
#import bcrypt
import pytesseract
from pigge.models import db, Parent

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    """Check if valid file selected"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_name(name, scanned_text):
    """Check input name with scanned file"""
    names = name.split()
    flag = False
    for i in names:
        if i.lower() in scanned_text.lower():
            flag = True
    return flag


def return_answer(answer):
    '''Return output'''
    if answer:
        return "Verification Successful. Login to continue."
    else:
        return "Verification Failed. Login to try again."


def verify_id(name, file_path):
    '''Input name and file path. Output is string to be displayed'''
    img = cv2.imread(file_path)
    cv2.Canny(img, 100, 200)
    scanned_text = pytesseract.image_to_string(img)
    result = check_name(name, scanned_text)
    return result


def cal_name(n):
    '''Encode name'''
    order = ord(n) - 64
    return "{0:0=2d}".format(order)


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

    if mail and phno:
        return False

    return True

'''
def generate_password(password):
    parent_password = bcrypt.hashpw(password, bcrypt.gensalt())
    print(parent_password)
    return parent_password


def verify_password(ppassword, password_hash):
    return bcrypt.checkpw(ppassword, password_hash)
'''