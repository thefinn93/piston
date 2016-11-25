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
import logging
from flask import Flask, render_template, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from raven.contrib.flask import Sentry

import piston.csrf
from piston.version import __version__

app = Flask(__name__)

app.config['USER_AGENT'] = "Piston/%s" % __version__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SENTRY_CONFIG'] = {
    "release": __version__
}
app.config.from_pyfile("config.py", silent=True)
app.config.from_pyfile("/etc/piston/config.py", silent=True)


sentry = Sentry(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.jinja_env.globals['csrf_token'] = piston.csrf.generate_token
app.jinja_env.globals['public_dsn'] = sentry.client.get_public_dsn('https')
app.jinja_env.globals['piston_version'] = __version__

import piston.register  # noqa: E104
import piston.notifications  # noqa: E014

app.register_blueprint(piston.register.views.app, url_prefix="/register")
app.register_blueprint(piston.notifications.views.app, url_prefix="/notifications")


@app.route("/")
def index():
    """Render the index page."""
    return render_template("index.html")


@app.route('/serviceworker.js')
def serviceworker():
    """Send the serviceworker from the root."""
    return app.send_static_file('js/serviceworker.js')


@app.route('/docs')
def docs():
    """Render the documentation."""
    return render_template('docs.html')


@app.route("/manifest.json")
def manifest():
    """Send the manifest."""
    return jsonify({
        "name": "Piston",
        "short_name": "Piston",
        "icons": [
            {
                "src": "images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            }
        ],
        "start_url": "/",
        "display": "standalone",
        "gcm_sender_id": app.config['GCM_ID']
    })


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', event_id=g.sentry_event_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
