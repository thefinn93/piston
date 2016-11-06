#!/usr/bin/env python3
"""Run piston in debug mode bound to 0.0.0.0."""
import piston
from werkzeug.contrib.fixers import ProxyFix


piston.app.wsgi_app = ProxyFix(piston.app.wsgi_app)
piston.app.run(host='0.0.0.0', debug=True)
