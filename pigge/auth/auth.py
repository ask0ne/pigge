from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from werkzeug.utils import secure_filename
from pigge.models import *
from pigge.auth.reg import *
from pigge.auth.extras import *

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
        # Received password in binary form
        # Hashing now
        password = generate_password(password)
        # Check if email and phone number is unique, add new entry if true
        if check_unique_user(mobile, email):
            # Create entry into the database
            createParent(pname, mobile, email, password)
            return redirect(url_for("auth_bp.login"))
        else:
            # Duplicate email/phno
            flash("Account already exists! Please login to continue")
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
        kid_id = calculate_id(name, birthdate)
        file_ = request.files["file"]

        if name and file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            file_path = os.path.join('pigge/uploads', filename)
            file_.save(file_path)
            answer = verify_id(name, file_path)
            # Kid ID has been verified and can now access his account
            if answer:
                # Update parent table here and create wallet
                createKid(kid_id, name, birthdate, email, pin, gender)
                createWallet(kid_id)
                updateParent(session['user_email'], kid_id)
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
        parent_login = authenticateParent(pmail, ppassword)
        if parent_login > -1:
            # Authenticated.
            session['user_email'] = pmail
            if parent_login == 1
            # Kid wallet exists
            return redirect(url_for('pdash.parent_dashboard'))
            # Kid wallet not found
            return redirect(url_for('auth_bp.registration_kid'))
        else:
            # Not authenticated. Incorrect credetntials.
            flash("Incorrect email ID or password! ")
            return redirect(url_for('auth_bp.login'))


@auth_bp.route("/login-kid", methods=["POST"])
def login_kid():
    """Login Kid route"""
    if request.method == "POST":
        kmail = request.form.get('k_email')
        kpin = request.form.get("pin")
        kid_login = authenticateKid(kmail, kpin)
        if kid_login == 1:
            # Authenticated
            session['user_email'] = kmail
            return redirect(url_for('kdash.kid_dashboard'))
        elif kid_login == 0:
            # Incorrect pin. Tries < 5
            flash("Incorrect email or pin!")
            return redirect(url_for('auth_bp.login'))
        else:
            # Incorrect pin. Tries exceeded 5. Reset to 0 and redirected to homepage.
            return redirect(url_for('main'))


@auth_bp.route("/authenticate/", methods=["GET", "POST"])
def register_successful():
    """create user session here and ideally redirect to parent dashboard"""
    return render_template("auth/resultpage.html", result=request.args.get('data'))


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('main'))
