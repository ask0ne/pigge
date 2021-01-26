from flask import Blueprint, render_template, redirect, request, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename
from pigge.models import *
from pigge.auth.registration import *

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/registration/parent', methods=["GET", "POST"])
def registration_parent():
    """Parents registration form"""
    if request.method == "GET":
        return render_template("auth/registration.html")

    if request.method == "POST":
        # Collect parent form data here
        pname = request.form.get("pname")
        pname = pname.upper()
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = bytes(request.form.get("psw"), encoding="UTF-8")
        # Hashing
        password = generate_password(password)
        # Check if email and phone number is unique, add new entry if true
        if check_unique_user(mobile, email):
            session['user_email'] = email
            p_user = Parent(created_on=datetime.now(), parent_name=pname, phone_number=mobile,
                            parent_email=email, parent_password=password, acc_status=-1)
            db.session.add(p_user)
            db.session.commit()
            return redirect(url_for("auth_bp.registration_kid"))

        return redirect(url_for("auth_bp.registration_parent"))


@auth_bp.route("/registration/kid", methods=["GET", "POST"])
def registration_kid():
    """Registration kid route"""
    if request.method == "GET":
        return render_template("auth/registration-kid.html")

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
            file_path = os.path.join('pigge/uploads', filename)
            file_.save(file_path)
            answer = verify_id(name, file_path)
            # Kid ID has been verified and can now access his account
            if answer:
                k_user = Kid(kid_id=kid_, kid_name=name, kid_dob=birthdate,
                             kid_email=email, kid_pin=pin, kid_gender=gender, number_of_tries=0)
                db.session.add(k_user)

                # Update parent table here and create panel
                pmail = session['user_email']
                p_user = Parent.query.filter_by(parent_email=pmail).first()
                p_user.acc_status = 1
                p_user.parent_id = "P" + kid_[1:]
                wallet_ID = "W" + kid_[1:]
                wallet = Wallet(wallet_id=wallet_ID, balance=0, generated_on=datetime.now(), pay_request=False,
                                two_f_auth=-1, restrict_bal=-1)
                db.session.add(wallet)
                db.session.commit()
            return redirect(url_for('auth_bp.register_successful', data=return_answer(answer)))


@auth_bp.route("/login", methods=["GET"])
def login():
    """Login page loading"""
    if request.method == "GET":
        return render_template("auth/login.html")


@auth_bp.route("/login-parent", methods=["POST"])
def login_parent():
    """Login Parent route"""
    if request.method == "POST":
        pmail = request.form.get('p_email')
        ppassword = bytes(request.form.get('password'), encoding="UTF-8")
        user = Parent.query.filter_by(parent_email=pmail).first()
        password_hash = user.parent_password
        status = user.acc_status
        # Incorrect email or password
        if not (user and verify_password(ppassword, password_hash)):
            return redirect(url_for('auth_bp.login'))

        # Check account status to check if kid account exists or not
        if status != -1:
            session['user_email'] = pmail
            return redirect(url_for('pdash.parent_dashboard'))
        else:
            return redirect(url_for('auth_bp.registration_kid'))


@auth_bp.route("/login-kid", methods=["POST"])
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
                return redirect(url_for('auth_bp.login'))
            else:
                return redirect(url_for('main'))
        session['user_email'] = kmail
        user.number_of_tries = 0
        return redirect(url_for('kdash.kid_dashboard'))


@auth_bp.route("/authenticate/", methods=["GET", "POST"])
def register_successful():
    """create user session here and ideally redirect to parent dashboard"""
    return render_template("auth/resultpage.html", result=request.args.get('data'))


'''@auth_bp.route("")
def logout():
    session.clear()'''
