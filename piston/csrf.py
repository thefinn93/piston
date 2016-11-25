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
from functools import wraps
from flask import request, session, abort
import uuid
import logging

logger = logging.getLogger(__name__)


def token_required(f):
    """Require a CSRF token when making POST requests."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = session.get('_csrf_token', None)
            if token is None or token != request.form.get('_csrf_token'):
                logger.debug("Submitted token %s did not match session token %s",
                             request.form.get('_csrf_token'), token)
                abort(403)
        return f(*args, **kwargs)
    return decorated_function


def generate_token():
    """Renerate anti-CSRF tokens."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    return '<input type="hidden" name="_csrf_token" value="%s" />' % session['_csrf_token']
