'''Kid ID Verification Module'''
import os
import cv2
import pytesseract

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
        return "Student Verification Successful"
    else:
        return "Student Verification Failed. Please upload a better photo or recheck entered name."


def verify_id(name, file_path):
    '''Input name and file path. Output is string to be displayed'''
    img = cv2.imread(file_path)
    cv2.Canny(img, 100, 200)
    scanned_text = pytesseract.image_to_string(img)
    result = check_name(name, scanned_text)
    answer = return_answer(result)
    return answer
