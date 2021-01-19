'''pigge'''
import os
import datetime
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from pigge.models import *
from pigge.id_verify import verify_id, allowed_file, calculate_id, return_answer

# Flask APP configurations
APP = Flask(__name__)
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
UPLOAD_FOLDER = "pigge/uploads"
APP.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/trial'
db.init_app(APP)


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
        name = request.form["name"]
        birthdate = request.form["birthdate"]
        email = request.form['email']
        pin = request.form['pin']

        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

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
            if answer:
                k_user = Kid(kid_id=calculate_id(
                    name, birthdate), kid_name=name, kid_dob=birthdate, kid_email=email, kid_pin=pin)
                # Update parent table here
                db.session.add(k_user)
                db.session.commit()    
            return redirect(url_for('register_successful', data=return_answer(answer)))


@APP.route("/registration", methods=["GET", "POST"])
def registration():
    """parents reg form"""
    if request.method == "GET":
        return render_template("registration.html")
    if request.method == "POST":
        # Collect parent form data here
        pname = request.form.get("pname")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("psw")
        cr_on = datetime.datetime.now()
        p_user = Parent(created_on=cr_on, parent_name=pname, phone_number=mobile,
                        parent_email=email, parent_password=password, acc_status=False)
        db.session.add(p_user)
        db.session.commit()
        return redirect(url_for("registration_kid"))


@APP.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")


@APP.route("/", methods=["GET", "POST"])
def main():
    """main function"""
    if request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    APP.run(debug=True)
