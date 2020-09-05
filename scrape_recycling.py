from app import app, db
from models import RecyclingStreet, RecyclingEvent
from pprint import pprint
import datetime
from dateutil import parser, tz
import pytz
from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup
from sqlalchemy.sql import not_
from ics import Calendar
import requests

class ScrapeTown:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

def scrape():
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    min_date = now - datetime.timedelta(weeks=60)

    towns = list()
    towns.append(ScrapeTown('62.1', 'Goslar'))
    towns.append(ScrapeTown('62.4', 'Oker'))
    towns.append(ScrapeTown('62.5', 'Vienenburg'))

    for town in towns:
        scrape_streets(town)

    scrape_events(now)
    delete_old_events(min_date)

def scrape_streets(town):
    url = 'https://www.kwb-goslar.de/Abfallwirtschaft/Abfuhr/Online-Abfuhrkalender/index.php?ort=%s' % town.identifier
    print(url)

    response = urlopen(url)
    doc = BeautifulSoup(response, 'lxml')

    select = doc.find('select', {"name":"strasse"})

    for option in select.find_all('option'):
        if 'value' in option.attrs and option.attrs['value'].strip():
            street_id = option.attrs['value'].strip()
            street_name = option.text.strip()

            item = RecyclingStreet.query.filter_by(source_id = street_id).first()
            item_did_exist = False
            if item is None:
                item = RecyclingStreet(source_id = street_id)
            else:
                item_did_exist = True

            item.name = "%s, %s" % (street_name, town.name)
            item.town_id = town.identifier

            if not item_did_exist:
                db.session.add(item)

    db.session.commit()

def scrape_events(now):
    streets =  RecyclingStreet.query.all()
    years = [ now.strftime("%Y") ]

    in_six_month = now + datetime.timedelta(6*365/12)
    year_in_six_month = in_six_month.strftime("%Y")

    if year_in_six_month not in years:
        years.append(year_in_six_month)

    for street in streets:
        for year in years:
            scrape_events_for_street(street, year)

def scrape_events_for_street(street, year):
    try:
        street_id = street.source_id
        url = "https://www.kwb-goslar.de/output/abfall_export.php?csv_export=1&mode=vcal&ort=%s&strasse=%s&vtyp=4&vMo=1&vJ=%s&bMo=12" % (street.town_id, street_id, year)
        print(url)

        calendar = Calendar(requests.get(url).text)

        for event in calendar.events:
            event_id = event.uid
            category = event.name.split(':')[0]
            date = event.begin.datetime

            item = RecyclingEvent.query.filter_by(street_id = street.id, source_id = event_id).first()
            item_did_exist = False
            if item is None:
                item = RecyclingEvent(source_id = event_id)
            else:
                item_did_exist = True

            item.street_id = street.id
            item.category = category
            item.date = date

            if not item_did_exist:
                db.session.add(item)

    except Exception as e:
        pprint(url)
        pprint(e)
    finally:
        db.session.commit()

def delete_old_events(min_date):
    RecyclingEvent.query.filter(RecyclingEvent.date <= min_date).delete()
    RecyclingStreet.query.filter(not_(RecyclingStreet.events.any())).delete(synchronize_session=False)
    db.session.commit()

if __name__ == '__main__':
    scrape()