from datetime import datetime

import pytz

berlin_tz = pytz.timezone("Europe/Berlin")
gmt_tz = pytz.timezone("GMT")


def get_now():
    return datetime.now(tz=berlin_tz)


def get_today():
    now = get_now()
    return datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)


def create_berlin_date(year, month, day, hour=0, minute=0, second=0):
    return berlin_tz.localize(
        datetime(year, month, day, hour=hour, minute=minute, second=second)
    )


def create_gmt_date(year, month, day, hour=0, minute=0, second=0):
    return gmt_tz.localize(
        datetime(year, month, day, hour=hour, minute=minute, second=second)
    )
