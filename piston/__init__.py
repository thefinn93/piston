"""EasyPush is a tool to help send notifications from the web."""
from flask import Flask, render_template, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from raven.contrib.flask import Sentry


import piston.csrf

__version__ = "0.0.1"

app = Flask(__name__)

app.config['USER_AGENT'] = "Piston/%s" % __version__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile("config.py", silent=True)
app.config.from_pyfile("/etc/piston/config.py", silent=True)

sentry = Sentry(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.jinja_env.globals['csrf_token'] = piston.csrf.generate_token
app.jinja_env.globals['public_dsn'] = sentry.client.get_public_dsn('https')

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


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', event_id=g.sentry_event_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
