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
