"""Functions and endpoints related to registering for notifications from a site."""
from flask import Blueprint, request, jsonify

from piston.notifications.models import Notification
from piston.register.models import Registration
from piston import db

app = Blueprint('notification', __name__)


def serialize(notification):
    serialized = notification.__dict__
    if '_sa_instance_state' in serialized:
        del serialized['_sa_instance_state']
    return serialized


@app.route('/create', methods=["POST"])
def create():
    if request.authorization.username != "token":
        return jsonify({
            "error": "Unauthorized - authorization incorrect"
        }), 401

    notification = Notification(request.authorization.password, request.form.get("title"),
                                request.form.get("body"), request.form.get("url"))
    db.session.add(notification)
    db.session.commit()
    return jsonify({
        "success": True
    })


@app.route("/unread")
def unread():
    token = request.headers.get("X-Token")
    registration = Registration.query.filter_by(subscription_token=token).first()
    if registration is None:
        return jsonify({
            "error": "Invalid token"
        }), 401

    notifications = Notification.query.filter_by(registration=registration, read=False).all()
    return jsonify({
        "notifications": [serialize(n) for n in notifications]
    })
