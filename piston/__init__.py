"""EasyPush is a tool to help send notifications from the web."""
from flask import Flask, render_template, request, session, abort
import piston.register
import uuid

__version__ = "0.0.1"


app = Flask(__name__)

app.config['USER_AGENT'] = "Piston/%s" % __version__
app.config.from_pyfile("config.py")

app.register_blueprint(piston.register.app, url_prefix="/register")


@app.before_request
def csrf_protect():
    """Require a CSRF token when making POST requests."""
    if request.method == "POST":
        token = session.get('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            app.logger.debug("Submitted token %s did not match session token %s",
                             request.form.get('_csrf_token'), token)
            abort(403)


def generate_csrf_token():
    """Renerate anti-CSRF tokens."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    return '<input type="hidden" name="_csrf_token" value="%s" />' % session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.route("/")
def index():
    """Render the index page."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')