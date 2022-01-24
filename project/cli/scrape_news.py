import datetime
from pprint import pprint

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from sqlalchemy.sql import and_, not_

from project import db
from project.dateutils import get_now
from project.models import NewsItem


def scrape():
    now = get_now()
    min_date = now - datetime.timedelta(days=14)

    scrape_dwd(now)

    scrape_feed(
        now,
        min_date,
        "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
        "Stadt Goslar",
    )
    scrape_feed(
        now,
        min_date,
        "https://www.landkreis-goslar.de/media/rss/Pressemitteilung.xml",
        "Landkreis Goslar",
    )
    scrape_feed(
        now,
        min_date,
        "https://www.kwb-goslar.de/media/rss/Pressemitteilungen.xml",
        "KWB Goslar",
    )
    scrape_feed(
        now,
        min_date,
        "http://www.presseportal.de/rss/dienststelle_56518.rss2",
        "Polizei Goslar",
    )
    scrape_feed(
        now,
        min_date,
        "https://stadtbibliothek.goslar.de/stadtbibliothek/aktuelles?format=feed&type=rss",
        "Stadtbibliothek Goslar",
    )
    scrape_feed(
        now,
        min_date,
        "https://machmit.goslar.de/category/machmit-prozess/feed",
        "Mach mit!",
    )
    scrape_feed(now, min_date, "https://feuerwehr-goslar.de/feed/", "Feuerwehr Goslar")
    scrape_feed(
        now, min_date, "https://feuerwehr-vienenburg.de/feed/", "Feuerwehr Vienenburg"
    )
    scrape_feed(
        now, min_date, "https://feuerwehr-hahndorf.de/feed/", "Feuerwehr Hahndorf"
    )
    scrape_feed(
        now,
        min_date,
        "https://www.feuerwehr-wiedelah.de/rss/blog",
        "Feuerwehr Wiedelah",
    )
    scrape_feed(
        now,
        min_date,
        "http://www.ffw-jerstedt.de/index.php/einsaetze?format=feed&type=rss",
        "Feuerwehr Jerstedt",
    )
    scrape_feed(
        now,
        min_date,
        "https://www.feuerwehr-oker.de/index.php/aktuelles/einsaetze/einsatzberichte?format=feed&type=rss",
        "Feuerwehr Oker",
    )
    scrape_feed(
        now,
        min_date,
        "https://warnung.bund.de/bbk.mowas/rss/031530000000.xml",
        "Bevölkerungsschutz",
    )

    delete_old_items(min_date)


def upsert_news_item(entry_id, publisher_name, title, link, published, fetched):
    item = NewsItem.query.filter_by(source_id=entry_id).first()
    item_did_exist = False
    if item is None:
        item = NewsItem(source_id=entry_id)
    else:
        item_did_exist = True

    item.publisher_name = publisher_name
    item.content = title
    item.link_url = link
    item.published = published
    item.fetched = fetched

    if not item_did_exist:
        db.session.add(item)


def scrape_dwd(now):
    try:
        url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
        publisher_name = "Deutscher Wetterdienst"
        print(url)

        response = requests.get(url)
        doc = BeautifulSoup(response.text, "lxml")
        anchor = doc.find(id="Stadt Goslar")

        if anchor:
            upsert_news_item(
                "https://www.dwd.de",
                publisher_name,
                "Es liegen Wetterwarnungen vor",
                "https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html?ort=Goslar",
                now,
                now,
            )
        else:
            NewsItem.query.filter(NewsItem.publisher_name == publisher_name).delete(
                synchronize_session=False
            )

    except Exception as e:  # pragma: no cover
        pprint(e)
    finally:
        db.session.commit()


def scrape_feed(now, min_date, url, publisher_name):
    try:
        print(url)
        channel = feedparser.parse(url)
        entry_ids = list()

        for entry in channel.entries:

            if (
                "published" not in entry or "title" not in entry or "link" not in entry
            ):  # pragma: no cover
                continue

            title = entry.title
            if publisher_name == "Polizei Goslar":
                if title.startswith("POL-GS: "):
                    title = title[len("POL-GS: ") :]
                if "Goslar" not in title and "Vienenburg" not in title:
                    continue

            published = parser.parse(entry.published)
            if published < min_date or published > now:  # pragma: no cover
                continue

            entry_id = None
            if "id" in entry:
                entry_id = entry.id
            else:
                entry_id = entry.link

            upsert_news_item(
                entry_id, publisher_name, title, entry.link, published, now
            )
            entry_ids.append(entry_id)

        # Delete entries that are not part of the feed anymore
        NewsItem.query.filter(
            and_(
                NewsItem.publisher_name == publisher_name,
                not_(NewsItem.source_id.in_(entry_ids)),
            )
        ).delete(synchronize_session=False)

    except Exception as e:
        pprint(e)
    finally:
        db.session.commit()


def delete_old_items(min_date):
    NewsItem.query.filter(NewsItem.published <= min_date).delete()
    db.session.commit()
