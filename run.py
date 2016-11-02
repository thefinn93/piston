#!/usr/bin/env python3
"""Run piston in debug mode bound to 0.0.0.0."""
import piston
piston.app.run(host='0.0.0.0', debug=True)
