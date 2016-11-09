"""Models related to notifications."""
import json
from urllib.parse import urlparse

from piston import db
from piston.register.models import Registration
from piston.notifications import gcm


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'))
    registration = db.relationship('Registration')
    title = db.Column(db.String())
    body = db.Column(db.String())
    url = db.Column(db.String())
    read = db.Column(db.Boolean)

    def __init__(self, token, title, body=None, url=None, read=False):
        self.title = title
        self.body = body
        self.url = url
        self.read = read

        registration = Registration.query.filter_by(token=token).first()
        assert registration is not None, "Invalid token!"
        self.registration = registration
        self.send()

    def send(self):
        subscription = json.loads(self.registration.subscription)
        endpoint = urlparse(subscription.get("endpoint"))
        db.app.logger.debug("Preparing to send notification to endpoint %s", endpoint.netloc)
        if endpoint.netloc == "android.googleapis.com":
            gcm.send(subscription)
        else:
            raise UnknownEndpointException(endpoint)


class UnknownEndpointException(Exception):

    pass
