'''pigge'''
import os
import datetime
from flask import Flask, flash, request, redirect, render_template, url_for, session
from werkzeug.utils import secure_filename
from pigge.models import *
from pigge.registration import *
from pigge.session import theParent

# Flask APP configurations
APP = Flask(__name__)
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP.config['TEMPLATES_AUTO_RELOAD'] = True
APP.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/pigge'
APP.config['SECRET_KEY'] = "893939939dad6325f1ef99d13573cd067196ff2ca89d09ce95fa9a27e6750bd6"
db.init_app(APP)


@APP.route("/kid-dashboard", methods=["GET", "POST"])
def kid_dashboard():
    """Kid's dashboard code here"""
    return render_template("kids_dash.html")


@APP.route("/parent-dashboard", methods=["GET", "POST"])
def parent_dashboard():
    """Parent's dashboard code here"""
    mail = session['user_email']
    user = theParent(mail)
    return render_template("parent_dashboard.html", user=user.user)


@APP.route("/dashboard", methods=["GET", "POST"])
def register_successful():
    """create user session here and ideally redirect to parent dashboard"""
    return render_template("resultpage.html", result=request.args.get('data'))


@APP.route("/registration-kid", methods=["GET", "POST"])
def registration_kid():
    """Registration kid route"""
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
        file_ = request.files["file"]

        if name and file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            file_path = os.path.join(APP.config["UPLOAD_FOLDER"], filename)
            file_.save(file_path)
            answer = verify_id(name, file_path)
            # Kid ID has been verified and can now access his account
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
    """Parents registration form"""
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
        # Check if email and phone number is unique, add new entry if true
        if check_unique_user(mobile, email):
            p_user = Parent(created_on=cr_on, parent_name=pname, phone_number=mobile,
                            parent_email=email, parent_password=password, acc_status=False)
            db.session.add(p_user)
            db.session.commit()
            return redirect(url_for("registration_kid"))

        return redirect(url_for("registration"))


@APP.route("/login", methods=["GET"])
def login():
    """Login page loading"""
    if request.method == "GET":
        return render_template("login.html")


@APP.route("/login-parent", methods=["POST"])
def login_parent():
    """Login Parent route"""
    if request.method == "POST":
        pmail = request.form.get('p_email')
        ppassword = request.form.get('password')
        user = Parent.query.filter_by(parent_email=pmail).first()
        password = user.parent_password
        status = user.acc_status
        # Incorrect email or password
        if not user or ppassword != password:
            return redirect(url_for('login'))

        # Check account status to check if kid account exists or not
        if status:
            session['user_email'] = pmail
            return redirect(url_for('parent_dashboard'))
        else:
            return redirect(url_for('registration_kid'))


@APP.route("/login-kid", methods=["POST"])
def login_kid():
    """Login Kid route"""
    if request.method == "POST":
        kmail = request.form.get('k_email')
        kpin = request.form.get("pin")
        user = Kid.query.filter_by(kid_email=kmail).first()
        pin = user.kid_pin
        if not user:
            return redirect(url_for('login'))
        elif kpin != pin:
            if user.number_of_tries < 5:
                user.number_of_tries += 1
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return redirect(url_for('main'))
        session['user_email'] = kmail
        return redirect(url_for('main'))

def logout():
    session.clear()

@APP.route("/", methods=["GET"])
def main():
    """
    main function
    index page
    """
    if request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    APP.run(debug=True)
