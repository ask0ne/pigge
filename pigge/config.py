"""
Flask app configuration here
"""
import os

DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0
TEMPLATES_AUTO_RELOAD = True
UPLOAD_FOLDER = "pigge/uploads"
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/pigge'
SQLALCHEMY_TRACK_MODIFICATIONS = True
