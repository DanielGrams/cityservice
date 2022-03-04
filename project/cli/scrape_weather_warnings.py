import re
from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql import not_

from project import db
from project.dateutils import create_berlin_date, get_now
from project.models import WeatherWarning


def scrape():
    now = get_now()

    try:
        url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
        print(url)

        warning_ids = list()

        response = requests.get(url)
        doc = BeautifulSoup(response.text, "lxml")
        published = now

        last_updated_prefix = "Letzte Aktualisierung: "
        last_updated_element = doc.find("strong", text=re.compile(last_updated_prefix))
        if last_updated_element:
            last_updated_str = last_updated_element.text.replace(
                last_updated_prefix, ""
            )
            published = _parse_date_time(now, last_updated_str)

        anchor = doc.find(id="Stadt Goslar")
        if anchor and anchor.nextSibling and anchor.nextSibling.name == "table":
            table = anchor.nextSibling
            table_rows = table.find_all("tr", recursive=False)

            for table_row in table_rows:
                table_cols = table_row.find_all("td")

                if len(table_cols) != 4:  # pragma: no cover
                    continue

                try:
                    (headline, start_str, end_str, content) = [
                        c.text for c in table_cols
                    ]
                    start = _parse_date_time(now, start_str)
                    end = _parse_date_time(now, end_str)

                    warning = WeatherWarning.query.filter_by(
                        headline=headline, content=content, start=start, end=end
                    ).first()

                    if warning is None:
                        warning = WeatherWarning(
                            headline=headline, content=content, start=start, end=end
                        )
                        db.session.add(warning)
                        db.session.flush()

                    warning.published = published
                    warning_ids.append(warning.id)
                except Exception as e:  # pragma: no cover
                    pprint(e)

        # Delete entries that are not part of the feed anymore
        WeatherWarning.query.filter(not_(WeatherWarning.id.in_(warning_ids))).delete(
            synchronize_session=False
        )

    except Exception as e:  # pragma: no cover
        pprint(e)
    finally:
        db.session.commit()


def _parse_date_time(now: datetime, input: str) -> datetime:
    # Fr, 04. Mär, 07:33 Uhr
    regex = r"\w{2}, (\d{2})\. (.{3}), (\d{2}):(\d{2})"
    match = re.search(regex, input)
    day_str, month_str, hour_str, minute_str = match.groups()

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
