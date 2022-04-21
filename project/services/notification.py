import datetime
import json

from py_vapid import Vapid
from pywebpush import WebPushException, webpush
from sqlalchemy.sql import and_

from project import app, db
from project.dateutils import get_today
from project.models import PushRegistration, RecyclingEvent, User


def send_notification(registration: PushRegistration, message: str) -> bool:
    try:
        send_web_push(registration, message)
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


def send_web_push(registration: PushRegistration, message: str):  # pragma: no cover
    private_key_str = app.config["VAPID_PRIVATE_KEY"]
    private_key = Vapid.from_pem(private_key_str.encode("utf8"))

    webpush(
        subscription_info=json.loads(registration.token),
        data=message,
        vapid_private_key=private_key,
        vapid_claims={"sub": "mailto:{}".format(app.config["VAPID_CLAIM_EMAIL"])},
    )


def send_recycling_events() -> tuple:
    # Aufruf 18:00 Uhr am Vortag
    today = get_today()
    min_date = today + datetime.timedelta(days=1)
    max_date = min_date

    success_count = 0
    error_count = 0
    users = User.query.all()
    for user in users:
        for recycling_street in user.recyclingstreets:
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
                    if send_notification(push_registration, message):
                        success_count = success_count + 1
                    else:  # pragma: no cover
                        error_count = error_count + 1

    return success_count, error_count
