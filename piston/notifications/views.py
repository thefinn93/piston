"""Functions and endpoints related to registering for notifications from a site."""
from flask import Blueprint, request, jsonify

from piston.notifications import models
from piston import db

app = Blueprint('notification', __name__)


@app.route('/create', methods=["POST"])
def create():
    if request.authorization.username != "token":
        return jsonify({
            "error": "Unauthorized - authorization incorrect"
        }), 401

    registration = models.Notification(request.authorization.password, request.form.get("title"),
                                       request.form.get("body"), request.form.get("url"))
    db.session.add(registration)
    db.session.commit()
    return "mk"
