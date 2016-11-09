"""Models related to registrations."""
import string
import random
import json

from piston import db


alphabet = string.ascii_letters + string.digits + "-._"


def gentoken(len):
    """Generate a secure(ish) random token."""
    return ''.join(random.choice(alphabet) for i in range(len))


class Registration(db.Model):
    """Remote sites wishing to send content to users, and the GCM IDs to send them to."""

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    domain = db.Column(db.String(120), nullable=False)
    subscription = db.Column(db.String(500), nullable=False)
    subscription_token = db.Column(db.String)
    enabled = db.Column(db.Boolean, default=True)

    def __init__(self, domain, subscription, name, token=None, enabled=True):
        self.domain = domain
        self.subscription = subscription
        self.name = name if name is not None else domain
        self.token = token if token is not None else gentoken(64)
        self.enabled = enabled
        try:
            subscription = json.loads(subscription)
            self.subscription_token = subscription.get("endpoint").split("/")[-1]
        except ValueError:
            pass

    def __repr__(self):
        return '<Registration %r>' % self.domain
