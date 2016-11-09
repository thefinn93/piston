"""EasyPush is a tool to help send notifications from the web."""
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

import piston.csrf

__version__ = "0.0.1"

app = Flask(__name__)

app.config['USER_AGENT'] = "Piston/%s" % __version__
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

app.jinja_env.globals['csrf_token'] = piston.csrf.generate_token

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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
