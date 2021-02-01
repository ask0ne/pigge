'''pigge'''
from flask import Flask, request, render_template
from pigge.models import db
from pigge.auth.auth import auth_bp
from pigge.pdash.pdash import pdash_bp
from pigge.kdash.kdash import kdash_bp
from pigge.payment.payment import payment_bp

# Flask APP configurations
APP = Flask(__name__)
APP.config.from_pyfile('config.py')
APP.register_blueprint(auth_bp)
APP.register_blueprint(pdash_bp)
APP.register_blueprint(kdash_bp)
APP.register_blueprint(payment_bp)
db.init_app(APP)


@APP.route("/", methods=["GET"])
def main():
    """
    main function
    index page
    """
    if request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    APP.run()
