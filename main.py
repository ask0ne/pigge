"""LP2"""
import os
from flask import Flask, flash, request, redirect, render_template
import cv2
import pytesseract
from werkzeug.utils import secure_filename


APP = Flask(__name__, template_folder="static")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
APP.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


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

@APP.route("/", methods=["GET", "POST"])
def main():
    """main function"""
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        name = request.form["name"]

        if file.filename == "":
            flash("No file selected!")
            return redirect(request.url)

        if name == "":
            flash("Please enter your name!")
            return redirect(request.url)

        if name and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(APP.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            img = cv2.imread(file_path)
            cv2.Canny(img, 100, 200)
            scanned_text = pytesseract.image_to_string(img)
            print(scanned_text)
            result = check_name(name, scanned_text)
            answer = return_answer(result)
            return render_template("resultpage.html", result=answer)


if __name__ == "__main__":
    APP.run()
