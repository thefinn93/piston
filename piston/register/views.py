"""Functions and endpoints related to registering for notifications from a site."""
from flask import Blueprint, render_template, request
from urllib.parse import urlparse
import requests

import piston
from piston.register import exceptions

app = Blueprint('register', __name__)


def checkconfig(url):
    """Retreive a configuration from a given URL and ensure that it complies with the rules."""
    parsed_url = urlparse(url)

    if parsed_url.scheme != "https":
        raise exceptions.InsecureConfigSchemeException("config must be loaded over https!")

    config = requests.get(url, headers={"User-Agent": "Piston/%s" % piston.__version__}).json()

    if "redirect_url" not in config:
        raise exceptions.ConfigurationException("Your configuration is missing a redirect_url!",
                                                config)

    redirect = urlparse(config['redirect_url'])
    if redirect.scheme != "https":
        raise exceptions.InsecureRedirectException("The redirect_url must be https")

    # if redirect.netloc != parsed_url.netloc:
    #     raise DomainMismatchException("redirect_url and config_url must share a domain.")

    config['domain'] = redirect.netloc
    return config


@app.route("/")
def register_page():
    """Register a client to send notifications to."""
    try:
        config = checkconfig(request.args.get("config"))
        return render_template("register.html",
                               c=config,
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
        return render_template("post_register.html", redirect_url=request.form.get("redirect_url"),
                               registration=registration, nonce=request.form.get("nonce", None))
    else:
        return "okay, bye"
