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
