#!/usr/bin/env python3
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

import piston
from werkzeug.contrib.fixers import ProxyFix


piston.app.wsgi_app = ProxyFix(piston.app.wsgi_app)
piston.app.run(host='0.0.0.0', debug=True)
