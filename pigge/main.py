'''pigge'''
import os
import datetime
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from pigge.models import *
from pigge.id_verify import verify_id, allowed_file, calculate_id, return_answer, check_unique_user

# Flask APP configurations
APP = Flask(__name__)
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
UPLOAD_FOLDER = "pigge/uploads"
APP.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/pigge'
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
        name = name.upper()
        birthdate = request.form["birthdate"]
        email = request.form['email']
        pin = request.form['pin']
        gender = request.form['gender']
        kid_ = calculate_id(name, birthdate)
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
                k_user = Kid(kid_id=kid_, kid_name=name, kid_dob=birthdate,
                             kid_email=email, kid_pin=pin, kid_gender=gender, number_of_tries=0)
                db.session.add(k_user)
                # Update parent table here and create panel
                #parent = db.session.query(Parent).filter(Parent.id == 2).one()
                #parent.acc_status = True
                parent_ID = "P"
                parent_ID += kid_[1:]
                #parent.parent_id = parent_ID
                panel = Panel(parent_id=parent_ID, pay_request=False,
                              two_f_auth=-1, restrict_bal=-1)
                db.session.add(panel)
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
        pname = pname.upper()
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("psw")
        cr_on = datetime.datetime.now()
        if check_unique_user(mobile, email):
            p_user = Parent(created_on=cr_on, parent_name=pname, phone_number=mobile,
                            parent_email=email, parent_password=password, acc_status=False)
            db.session.add(p_user)
            db.session.commit()
            return redirect(url_for("registration_kid"))
        else:
            return redirect(url_for("registration"))


@APP.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")


@APP.route("/login-parent", methods=["POST"])
def login_parent():
    if request.method == "POST":
        pmail = request.form.get('p_email')
        ppassword = request.form.get('password')
        user = Parent.query.filter_by(parent_email=pmail).first()
        password = user.parent_password
        if not user or ppassword != password:
            return redirect(url_for('login'))

        return redirect(url_for('main'))


@APP.route("/login-kid", methods=["POST"])
def login_kid():
    if request.method == "POST":
        kmail = request.form.get('k_email')
        kpin = request.form.get("pin")
        user = Kid.query.filter_by(kid_email=kmail).first()
        pin = user.kid_pin
        if not user or kpin != pin:
            return redirect(url_for('login'))

        return redirect(url_for('main'))


@APP.route("/", methods=["GET", "POST"])
def main():
    """main function"""
    if request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    APP.run(debug=True)
