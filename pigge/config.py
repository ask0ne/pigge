"""
Flask app configuration here
"""
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0
TEMPLATES_AUTO_RELOAD = True
UPLOAD_FOLDER = "pigge/uploads"
SECRET_KEY = "893939939dad6325f1ef99d13573cd067196ff2ca89d09ce95fa9a27e6750bd6"
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/pigge'
SQLALCHEMY_TRACK_MODIFICATIONS = True
