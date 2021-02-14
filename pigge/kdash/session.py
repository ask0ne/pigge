"""Handling kid sessions"""
from pigge.models import db, Kid


class TheKid:
    """Initialize parent on login"""

    def __init__(self, mail):
        self.user = Kid.query.filter_by(kid_email=mail).first()


    def pay_service(self, val):
        pass

