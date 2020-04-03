from app import app, db
from models import NewsItem
import feedparser
from pprint import pprint
import datetime
from dateutil import parser, tz
import pytz

def scrape():
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    min_date = now - datetime.timedelta(days=14)

    scrape_feed(
        now,
        min_date,
        'https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss',
        'Stadt Goslar')
    scrape_feed(
        now,
        min_date,
        'https://www.landkreis-goslar.de/media/rss/Pressemitteilung.xml',
        'Landkreis Goslar')
    scrape_feed(
        now,
        min_date,
        'https://www.kwb-goslar.de/media/rss/Pressemitteilungen.xml',
        'KWB Goslar')
    scrape_feed(
        now,
        min_date,
        'http://www.presseportal.de/rss/dienststelle_56518.rss2',
        'Polizei Goslar')
    scrape_feed(
        now,
        min_date,
        'https://stadtbibliothek.goslar.de/stadtbibliothek/aktuelles?format=feed&type=rss',
        'Stadtbibliothek Goslar')
    scrape_feed(
        now,
        min_date,
        'https://machmit.goslar.de/category/machmit-prozess/feed',
        'Mach mit!')

    delete_old_items(min_date)

def scrape_feed(now, min_date, url, publisher_name):
    try:
        print(url)
        channel = feedparser.parse(url)

        for entry in channel.entries:

            if ('published' not in entry or
                'title' not in entry or
                'link' not in entry):
                continue

            published = parser.parse(entry.published)
            if published < min_date:
                continue

            entry_id = None
            if 'id' in entry:
                entry_id = entry.id
            else:
                entry_id = entry.link

            item = NewsItem.query.filter_by(source_id = entry_id).first()
            item_did_exist = False
            if item is None:
                item = NewsItem(source_id = entry_id)
            else:
                item_did_exist = True

            item.publisher_name = publisher_name
            item.content = entry.title
            item.link_url = entry.link
            item.published = published
            item.fetched = now

            if not item_did_exist:
                db.session.add(item)

    except Exception as e:
        pprint(e)
    finally:
        db.session.commit()

def delete_old_items(min_date):
    NewsItem.query.filter(NewsItem.published <= min_date).delete()
    db.session.commit()

if __name__ == '__main__':
    scrape()