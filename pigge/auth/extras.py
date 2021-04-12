"""
Contains extra functions necessary for auth module independant of the database.
"""
import os
import cv2
import bcrypt
import pytesseract

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\kawad\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'


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
    canny_img = cv2.Canny(img, 100, 200)
    scanned_text = pytesseract.image_to_string(canny_img)
    result = check_name(name, scanned_text)
    return result


def cal_name(n):
    '''Encode name'''
    order = ord(n) - 64
    return "{0:0=2d}".format(order)


def generate_password(password):
    parent_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return parent_password


def verify_password(ppassword, password_hash):
    return bcrypt.checkpw(ppassword, password_hash)
