import datetime
import json

from apns2.client import APNsClient
from apns2.errors import Unregistered
from apns2.payload import Payload
from flask import url_for
from py_vapid import Vapid
from pyfcm import FCMNotification
from pyfcm.errors import FCMNotRegisteredError
from pywebpush import WebPushException, webpush
from sqlalchemy.sql import and_

from project import apns_cert_path, app, db
from project.dateutils import get_today
from project.models import (
    PushPlatform,
    PushRegistration,
    RecyclingEvent,
    RecyclingStreetsUsers,
    User,
)


def send_notification(
    registration: PushRegistration, message: str, url: str = None
) -> bool:  # pragma: no cover
    try:
        if registration.platform == PushPlatform.web:
            send_web_push(registration, message, url)
        elif registration.platform == PushPlatform.ios:
            send_ios_push(registration, message, url)
        elif registration.platform == PushPlatform.android:
            send_android_push(registration, message, url)
        else:
            raise NotImplementedError()
        return True
    except WebPushException as ex:
        if ex.response and ex.response.status_code and ex.response.status_code == 410:
            db.session.delete(registration)
            db.session.commit()
            return False

        app.logger.exception(ex)
    except Unregistered:
        db.session.delete(registration)
        db.session.commit()
        return False
    except FCMNotRegisteredError:
        db.session.delete(registration)
        db.session.commit()
        return False
    except Exception as ex:
        app.logger.exception(ex)
        return False


def send_android_push(
    registration: PushRegistration, message: str, url: str = None
):  # pragma: no cover
    push_service = FCMNotification(app.config["FCM_API_KEY"])
    custom = {"url": url} if url else None
    result = push_service.notify_single_device(
        registration_id=registration.token, message_body=message, data_message=custom
    )

    if result["failure"] > 0:
        if result["results"] > 0:
            raise ConnectionError("FCM error", result["results"][0])
        raise ConnectionError("FCM error")


def send_ios_push(
    registration: PushRegistration, message: str, url: str = None
):  # pragma: no cover
    custom = {"url": url} if url else None
    payload = Payload(alert=message, sound="default", badge=1, custom=custom)
    app_id = app.config["APNS_APP_ID"]
    use_sandbox = app.config["APNS_USE_SANDBOX"]
    client = APNsClient(
        apns_cert_path, use_sandbox=use_sandbox, use_alternative_port=False
    )
    client.send_notification(registration.token, payload, app_id)


def send_web_push(
    registration: PushRegistration, message: str, url: str = None
):  # pragma: no cover
    private_key_str = app.config["VAPID_PRIVATE_KEY"]
    private_key = Vapid.from_pem(private_key_str.encode("utf8"))
    data = {"options": {"body": message}}

    if url:
        data["options"]["data"] = {"url": url}

    webpush(
        subscription_info=json.loads(registration.token),
        data=json.dumps(data),
        vapid_private_key=private_key,
        vapid_claims={"sub": "mailto:{}".format(app.config["VAPID_CLAIM_EMAIL"])},
    )


def send_recycling_events() -> tuple:
    # Aufruf 18:00 Uhr am Vortag
    today = get_today()
    min_date = today + datetime.timedelta(days=1)
    max_date = min_date
    base_url = url_for("frontend.index", _external=True)

    success_count = 0
    error_count = 0
    users = User.query.all()

    for user in users:
        user_recycling_streets = (
            RecyclingStreetsUsers.query.with_parent(user)
            .filter(RecyclingStreetsUsers.notifications_active)
            .all()
        )

        for user_recycling_street in user_recycling_streets:
            recycling_street = user_recycling_street.recyclingstreet
            recycling_street_url = f"{base_url}recycling-streets/{recycling_street.id}"
            next_events = RecyclingEvent.query.filter(
                and_(
                    RecyclingEvent.street_id == recycling_street.id,
                    RecyclingEvent.date <= min_date,
                    RecyclingEvent.date >= max_date,
                )
            ).all()

            for next_event in next_events:
                for push_registration in user.push_registrations:
                    message = f"{recycling_street.name}: {next_event.category}"
                    if send_notification(
                        push_registration, message, recycling_street_url
                    ):
                        success_count = success_count + 1
                    else:  # pragma: no cover
                        error_count = error_count + 1

    return success_count, error_count
