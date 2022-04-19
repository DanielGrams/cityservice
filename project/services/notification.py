import json

from py_vapid import Vapid
from pywebpush import WebPushException, webpush

from project import app, db
from project.models import PushRegistration


def send_notification(registration: PushRegistration, message: str):
    try:
        send_web_push(registration, message)
    except WebPushException as ex:
        if ex.response and ex.response.status_code and ex.response.status_code == 410:
            db.session.delete(registration)
            db.session.commit()
            return

        app.logger.exception(ex)  # pragma: no cover


def send_web_push(registration: PushRegistration, message: str):  # pragma: no cover
    private_key_str = app.config["VAPID_PRIVATE_KEY"]
    private_key = Vapid.from_pem(private_key_str.encode("utf8"))

    webpush(
        subscription_info=json.loads(registration.token),
        data=message,
        vapid_private_key=private_key,
        vapid_claims={"sub": "mailto:{}".format(app.config["VAPID_CLAIM_EMAIL"])},
    )
