import datetime
import json

from flask import url_for
from py_vapid import Vapid
from pywebpush import WebPushException, webpush
from sqlalchemy.sql import and_

from project import app, db
from project.dateutils import get_today
from project.models import PushRegistration, RecyclingEvent, RecyclingStreetsUsers, User


def send_notification(
    registration: PushRegistration, message: str, url: str = None
) -> bool:
    try:
        send_web_push(registration, message, url)
        return True
    except WebPushException as ex:
        if ex.response and ex.response.status_code and ex.response.status_code == 410:
            db.session.delete(registration)
            db.session.commit()
            return False

        app.logger.exception(ex)  # pragma: no cover
    except Exception as ex:  # pragma: no cover
        app.logger.exception(ex)
        return False


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
