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

from flask import Blueprint, render_template, request, url_for, current_app
from urllib.parse import urlparse

import piston
from piston.register import exceptions

app = Blueprint('register', __name__)


def checkconfig():
    """Retreive a configuration from a given URL and ensure that it complies with the rules."""
    config = request.args.copy()
    if "desktop" in config:
        if "name" not in config:
            raise exceptions.ConfigurationException("You must specify a name for desktop tokens!")
    elif "redirect_url" not in config:
        raise exceptions.ConfigurationException("You're is missing a redirect_url!")
    else:
        redirect = urlparse(config['redirect_url'])
        if redirect.scheme != "https":
            raise exceptions.InsecureRedirectException("The redirect_url must be https")
        config['domain'] = redirect.netloc
    return config


@app.route("/")
def register_page():
    """Register a client to send notifications to."""
    try:
        config = checkconfig()
        return render_template("register.html",
                               c=config,
                               desktop="desktop" in config,
                               root=request.headers['Host'])
    except exceptions.ConfigurationException as e:
        return render_template("error.html", error=e)


@app.route("/next", methods=["POST"])
@piston.csrf.token_required
def post_register():
    """Accept or deny the registration request."""
    if request.form.get("action") is None:
        redirect = urlparse(request.form.get("redirect_url"))
        subscription = request.form.get("subscription")
        registration = piston.register.models.Registration(domain=redirect.netloc,
                                                           name=request.form.get("name"),
                                                           subscription=subscription)
        piston.db.session.add(registration)
        piston.db.session.commit()
        token = "https://%s:%s@%s%s" % ("token", registration.token,
                                        current_app.config.get("SERVER_NAME", "localhost"),
                                        url_for('notification.create'))
        return render_template("post_register.html", redirect_url=request.form.get("redirect_url"),
                               registration=registration, token=token,
                               name=request.form.get('name'),
                               nonce=request.form.get("nonce"))
    else:
        return "okay, bye"
