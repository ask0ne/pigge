"""Handling parent sessions"""
from pigge.models import Parent


class TheParent:
    """Initialize parent on login"""

    def __init__(self, mail):
        self.user = Parent.query.filter_by(parent_email=mail).first()

    def limit_transaction(self, val):
        try:
            self.user.restrict_bal = val
            return True
        except NameError:
            return False

    def add_funds(self, val):
        pass
