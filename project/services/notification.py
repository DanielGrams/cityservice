import json

from py_vapid import Vapid
from pywebpush import WebPushException, webpush

from project import app
from project.models import PushRegistration


def send_notification(registration: PushRegistration, message: str):  # pragma: no cover
    private_key_str = app.config["VAPID_PRIVATE_KEY"]
    private_key = Vapid.from_pem(private_key_str.encode("utf8"))

    try:
        webpush(
            subscription_info=json.loads(registration.token),
            data=message,
            vapid_private_key=private_key,
            vapid_claims={"sub": "mailto:{}".format(app.config["VAPID_CLAIM_EMAIL"])},
        )
    except WebPushException as ex:
        if ex.response and ex.response.json():
            extra = ex.response.json()
            raise Exception(
                "Remote service replied with a {}:{}, {}",
                extra.code,
                extra.errno,
                extra.message,
            )
