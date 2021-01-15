'''pigge'''
import os
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from pigge.models import db
from pigge.id_verify import verify_id

# Flask APP configurations
APP = Flask(__name__)
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP.config['DEBUG'] = True
UPLOAD_FOLDER = "pigge/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
APP.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/pigge'
db.init_app(APP)


def allowed_file(filename):
    """Check if valid file selected"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route("/kids-dashboard", methods=["GET", "POST"])
def kids_dashboard():
    """Kid's dashboard code here"""
    return render_template("kids_dash.html")


@APP.route("/dashboard", methods=["GET", "POST"])
def register_successful():
    """create user session here and ideally redirect to parent dashboard"""
    return render_template("resultpage.html", result=request.args.get('data'))


@APP.route("/registration-kid", methods=["GET", "POST"])
def registration_kid():
    """main function"""
    if request.method == "GET":
        return render_template("registration-kid.html")

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
            answer = verify_id(name, file_path)
            return redirect(url_for('register_successful', data=answer))


@APP.route("/registration", methods=["GET", "POST"])
def registration():
    """parents reg form"""
    if request.method == "GET":
        return render_template("registration.html")
    if request.method == "POST":
        # Collect parent form data here
        return redirect(url_for("registration_kid"))


@APP.route("/", methods=["GET", "POST"])
def main():
    """main function"""
    if request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    APP.run()
