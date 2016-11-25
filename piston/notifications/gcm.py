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


import json
import requests
import logging

from piston import db

logger = logging.getLogger(__name__)


def send(subscription):
    gcm_url = "/".join(subscription.get("endpoint").split("/")[:-1])
    gcm_registration = subscription.get("endpoint").split("/")[-1]
    headers = {
        "User-Agent": db.app.config.get("USER_AGENT"),
        "Authorization": "key=%s" % db.app.config.get("GCM_KEY"),
        "Content-Type": "application/json"
    }
    postdata = json.dumps({"registration_ids": [gcm_registration]})
    result = requests.post(gcm_url, postdata, headers=headers).content
    logger.debug("Got response from GCM: %r", result)
