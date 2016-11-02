"""Functions and endpoints related to registering for notifications from a site."""
from flask import Blueprint, render_template, request
from urllib.parse import urlparse
import requests
import piston

app = Blueprint('register', __name__)


def checkconfig(url):
    """Retreive a configuration from a given URL and ensure that it complies with the rules."""
    parsed_url = urlparse(url)

    if parsed_url.scheme != "https":
        raise InsecureConfigSchemeException("config must be loaded over https!")

    config = requests.get(url, headers={"User-Agent": "Piston/%s" % piston.__version__}).json()

    if "redirect_url" not in config:
        raise ConfigurationException("Your configuration is missing a redirect_url!", config)

    redirect = urlparse(config['redirect_url'])
    if redirect.scheme != "https":
        raise InsecureRedirectException("The redirect_url must be https")

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
    except ConfigurationException as e:
        return render_template("error.html", error=e)


@app.route("/next", methods=["POST"])
def post_register():
    """Accept or deny the registration request."""
    if request.form.get("action") == "Allow":
        return render_template("post_register.html", redirect_url=request.form.get("redirect_url"),
                               token="blah", nonce=request.form.get("nonce", None))
    else:
        return "okay, bye"


class ConfigurationException(Exception):
    """A given configuration file is invalid."""

    pass


class InsecureConfigSchemeException(ConfigurationException):
    """The provided config URL is not over https."""

    pass


class ConfigurationMissingKeysException(ConfigurationException):
    """The provided config URL is missing required keys."""

    pass


class InsecureRedirectException(ConfigurationException):
    """The provided redirect URL is not over https."""

    pass


class DomainMismatchException(ConfigurationException):
    """The provided config URL and the redirect URL do not share a domain."""

    pass
