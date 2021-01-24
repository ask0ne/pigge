"""Handles Kid Dashboard functionality"""
from flask import Blueprint, render_template

kdash_bp = Blueprint('kdash', __name__, template_folder='templates')

@kdash_bp.route("/kid-dashboard", methods=["GET", "POST"])
def kid_dashboard():
    """Kid's dashboard code here"""
    return render_template("kdash/kids_dash.html")