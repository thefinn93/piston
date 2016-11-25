"""
This file is part of Piston.

Piston is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Piston is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Piston.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
from urllib.parse import urlparse

from piston import db
from piston.register.models import Registration
from piston.notifications import exceptions
from piston.notifications import gcm


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'))
    registration = db.relationship('Registration')
    title = db.Column(db.String())
    body = db.Column(db.String())
    url = db.Column(db.String())
    properties = db.Column(db.String())
    read = db.Column(db.Boolean)

    def __init__(self, token, title, body=None, properties=None, url=None, read=False):
        self.title = title
        self.body = body
        if "actions" in properties:
            properties['actions'] = json.loads(properties['actions'])
        self.properties = json.dumps(properties)
        self.url = url
        self.read = read

        registration = Registration.query.filter_by(token=token).first()
        if registration is None:
            raise exceptions.InvalidTokenException()
        self.registration = registration
        self.send()

    def send(self):
        subscription = json.loads(self.registration.subscription)
        endpoint = urlparse(subscription.get("endpoint"))
        db.app.logger.debug("Preparing to send notification to endpoint %s", endpoint.netloc)
        if endpoint.netloc == "android.googleapis.com":
            gcm.send(subscription)
        else:
            raise exceptions.UnknownEndpointException(endpoint)
