import datetime

import requests
from bs4 import BeautifulSoup
from ics import Calendar
from sqlalchemy.sql import and_, not_
from sqlalchemy.sql.expression import func

from project import app, db
from project.dateutils import get_now
from project.models import Place, RecyclingEvent, RecyclingStreet
from project.utils import get_content_from_response

# Town IDs vor 2022
# towns.append(ScrapeTown('62.1', 'Goslar'))
# towns.append(ScrapeTown('62.4', 'Oker'))
# towns.append(ScrapeTown('62.5', 'Vienenburg'))

# Town IDs ab 2022
# towns.append(ScrapeTown("2523.1", "Goslar"))
# towns.append(ScrapeTown("2523.8", "Oker"))
# towns.append(ScrapeTown("2523.10", "Vienenburg"))


class ScrapeTown:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name


def scrape():
    now = get_now()
    min_date = now - datetime.timedelta(weeks=60)

    id_to_name_mapping = scrape_index()
    places = Place.query.filter(Place.recycling_ids.isnot(None)).all()
    for place in places:
        scrape_place(place, id_to_name_mapping)

    scrape_events()
    delete_old_events(min_date)


def scrape_index() -> dict:
    url = (
        "https://www.kwb-goslar.de/Abfallwirtschaft/Abfuhr/Online-Abfuhrkalender-2022/"
    )
    result = dict()

    try:
        response = requests.get(url, headers={"referer": "https://www.kwb-goslar.de"})
        html = get_content_from_response(response)
        doc = BeautifulSoup(html, features="html.parser")
        options = doc.find(id="sf_locid").find_all("option")

        for option in options:
            value = option.get("value").strip()

            if len(value) > 0:
                result[value] = option.text.strip()

    except Exception:  # pragma: no cover
        app.logger.exception(url)

    return result


def scrape_place(place: Place, id_to_name_mapping: dict):
    ids = place.recycling_ids.split(",")
    towns = list()

    for id in ids:
        if id in id_to_name_mapping:
            towns.append(ScrapeTown(id, id_to_name_mapping[id]))
        else:  # pragma: no cover
            app.logger.warning(f"Recycling id {id} of place {place.name} not found")

    for town in towns:
        scrape_streets(place, town)


def scrape_streets(place: Place, town: ScrapeTown):
    try:
        url = (
            "https://www.kwb-goslar.de/output/autocomplete.php?out=json&type=abto&mode=&select=2&refid=%s&term="
            % town.identifier
        )
        print(url)

        response = requests.get(url, headers={"referer": "https://www.kwb-goslar.de"})
        json = response.json()
        replace_from = " (%s)" % town.name
        replace_to = ", %s" % town.name

        for line in json:
            street_id = line[0].strip()
            street_name = line[1].strip()

            item = RecyclingStreet.query.filter(
                and_(
                    RecyclingStreet.place_id == place.id,
                    RecyclingStreet.source_id == street_id,
                    RecyclingStreet.town_id == town.identifier,
                )
            ).first()
            item_did_exist = False
            if item is None:
                item = RecyclingStreet(place_id=place.id, source_id=street_id)
            else:
                item_did_exist = True

            item.name = street_name.replace(replace_from, replace_to)
            item.town_id = town.identifier

            if not item_did_exist:
                db.session.add(item)

    except Exception:
        app.logger.exception(url)
    finally:
        db.session.commit()


def scrape_events():
    streets = RecyclingStreet.query.filter(
        func.length(RecyclingStreet.town_id) > 4
    ).all()  # > 4 bedeutet TownId ab 2022

    for street in streets:
        event_ids = list()
        scrape_events_for_street(street, event_ids)
        delete_events_not_in_calendars(street.id, event_ids)


def scrape_events_for_street(street, event_ids):
    try:
        street_id = street.source_id
        url = (
            "https://www.kwb-goslar.de/output/options.php?ModID=48&call=ical&pois=%s&alarm=0"
            % street_id
        )
        print(url)

        calendar = Calendar(
            requests.get(url, headers={"referer": "https://www.kwb-goslar.de"}).text
        )

        for event in calendar.events:
            event_id = event.uid
            category = event.name.split(":")[0]

            # Legacy
            date = event.begin.datetime.replace(
                hour=0
            ) + event.begin.datetime.tzinfo.utcoffset(event.begin.datetime)

            item = RecyclingEvent.query.filter_by(
                street_id=street.id, source_id=event_id
            ).first()
            item_did_exist = False
            if item is None:
                item = RecyclingEvent(source_id=event_id)
            else:
                item_did_exist = True

            item.street_id = street.id
            item.category = category
            item.date = date

            if not item_did_exist:
                db.session.add(item)

            event_ids.append(event_id)

    except Exception:
        app.logger.exception(url)
    finally:
        db.session.commit()


def delete_old_events(min_date):
    RecyclingEvent.query.filter(RecyclingEvent.date <= min_date).delete()
    RecyclingStreet.query.filter(not_(RecyclingStreet.events.any())).delete(
        synchronize_session=False
    )
    db.session.commit()


def delete_events_not_in_calendars(street_id, event_ids):
    # Delete events that are not part of the streets calendars anymore
    RecyclingEvent.query.filter(
        and_(
            RecyclingEvent.street_id == street_id,
            not_(RecyclingEvent.source_id.in_(event_ids)),
        )
    ).delete(synchronize_session=False)
    db.session.commit()
