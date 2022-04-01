import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql import not_

from project import app, db
from project.dateutils import create_berlin_date, get_now
from project.models import Place, WeatherWarning
from project.utils import get_content_from_response


def scrape():
    now = get_now()

    try:
        url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
        print(url)

        warning_ids = list()

        response = requests.get(
            url,
            headers={
                "Host": "www.dwd.de",
                "Accept": "*/*",
                "User-Agent": "curl/7.77.0",
            },
        )

        html = get_content_from_response(response)
        doc = BeautifulSoup(html, features="html.parser")
        published = now

        last_updated_prefix = "Letzte Aktualisierung: "
        last_updated_element = doc.find("strong", text=re.compile(last_updated_prefix))
        if last_updated_element:
            last_updated_str = last_updated_element.text.replace(
                last_updated_prefix, ""
            )
            published = _parse_date_time(now, last_updated_str)

        # Scrape all places
        places = Place.query.filter(Place.weather_warning_name.isnot(None)).all()
        for place in places:
            scrape_place(place, doc, now, published, warning_ids)

        # Delete entries that are not part of the feed anymore
        WeatherWarning.query.filter(not_(WeatherWarning.id.in_(warning_ids))).delete(
            synchronize_session=False
        )

    except Exception:  # pragma: no cover
        app.logger.exception(url)
    finally:
        db.session.commit()


def scrape_place(
    place: Place,
    doc: BeautifulSoup,
    now: datetime,
    published: datetime,
    warning_ids: list,
):
    anchor = doc.find(id=place.weather_warning_name)

    if anchor and anchor.nextSibling and anchor.nextSibling.name == "table":
        table = anchor.nextSibling
        table_rows = table.find_all("tr")

        for table_row in table_rows:
            table_cols = table_row.find_all("td")

            if len(table_cols) != 4:  # pragma: no cover
                continue

            try:
                (headline, start_str, end_str, content) = [c.text for c in table_cols]
                start = _parse_date_time(now, start_str)
                end = _parse_date_time(now, end_str)

                warning = WeatherWarning.query.filter_by(
                    place_id=place.id,
                    headline=headline,
                    content=content,
                    start=start,
                    end=end,
                ).first()

                if warning is None:
                    warning = WeatherWarning(
                        place_id=place.id,
                        headline=headline,
                        content=content,
                        start=start,
                        end=end,
                    )
                    db.session.add(warning)
                    db.session.flush()

                warning.published = published
                warning_ids.append(warning.id)
            except Exception:  # pragma: no cover
                app.logger.exception(place.id)


def _parse_date_time(now: datetime, input: str) -> datetime:
    # Do., 31. März, 07:49 Uhr
    # Fr, 04. Mär, 07:33 Uhr
    # Fr., 01. Apr., 07:17 Uhr
    regex = r"\w{2}\.?, (\d{2})\. ([^,]{3,}), (\d{2}):(\d{2})"
    match = re.search(regex, input)
    day_str, month_str, hour_str, minute_str = match.groups()
    month_str = month_str[:3]

    months = {
        "Jan": 1,
        "Feb": 2,
        "Mär": 3,
        "Apr": 4,
        "Mai": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Okt": 10,
        "Nov": 11,
        "Dez": 12,
    }
    month = months[month_str]

    result = create_berlin_date(
        now.year, month, int(day_str), int(hour_str), int(minute_str)
    )

    age = now - result
    if age.days > 180:
        result = create_berlin_date(
            result.year + 1, result.month, result.day, result.hour, result.minute
        )

    return result
