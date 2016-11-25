"""Functions and endpoints related to registering for notifications from a site."""
from flask import Blueprint, request, jsonify
import json

from piston.notifications.models import Notification
from piston.register.models import Registration
from piston import db
from piston import exceptions

app = Blueprint('notification', __name__)


def serialize(notification):
    serialized = notification.__dict__.copy()
    if '_sa_instance_state' in serialized:
        del serialized['_sa_instance_state']
    try:
        for key, value in json.loads(serialized.get('properties')).items():
            serialized[key] = value
    except (ValueError, TypeError):
        pass
    return serialized


@app.route('/create', methods=["POST"])
def create():
    try:
        properties = request.form.copy()
        properties.pop('title', None)
        properties.pop('body', None)
        properties.pop('url', None)
        notification = Notification(request.authorization.password, request.form.get("title"),
                                    request.form.get("body"), properties, request.form.get("url"))
        db.session.add(notification)
        db.session.commit()
        return jsonify({
            "success": True
        })
    except exceptions.PistonException as e:
        return jsonify(e.__dict__()), e.status_code


@app.route("/unread")
def unread():
    try:
        token = request.headers.get("X-Token")
        registration = Registration.query.filter_by(subscription_token=token).first()
        notifications = Notification.query.filter_by(registration=registration, read=False).all()
        results = []
        for notification in notifications:
            serialized = serialize(notification)
            notification.read = True
            db.app.logger.debug(serialized)
            results.append(serialized)
        db.session.commit()
        return jsonify({"notifications": results})
    except exceptions.PistonException as e:
        return jsonify(e.__dict__()), e.status_code
