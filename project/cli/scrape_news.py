import datetime
import re
from pprint import pprint

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from sqlalchemy.sql import and_, not_

from project import db
from project.dateutils import get_now
from project.models import NewsFeed, NewsItem


def scrape():
    now = get_now()
    min_date = now - datetime.timedelta(days=14)

    scrape_dwd(now)

    news_feeds = list()
    news_feeds.append(
        NewsFeed(
            publisher="Stadt Goslar",
            url="https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Landkreis Goslar",
            url="https://www.landkreis-goslar.de/media/rss/Pressemitteilung.xml",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="KWB Goslar",
            url="https://www.kwb-goslar.de/media/rss/Pressemitteilungen.xml",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Polizei Goslar",
            url="http://www.presseportal.de/rss/dienststelle_56518.rss2",
            title_filter=".*Goslar|Vienenburg.*",
            title_sub_pattern="POL-GS: ",
            title_sub_repl="",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Stadtbibliothek Goslar",
            url="https://stadtbibliothek.goslar.de/stadtbibliothek/aktuelles?format=feed&type=rss",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Mach mit!",
            url="https://machmit.goslar.de/category/machmit-prozess/feed",
        )
    )
    news_feeds.append(
        NewsFeed(publisher="Feuerwehr Goslar", url="https://feuerwehr-goslar.de/feed/")
    )
    news_feeds.append(
        NewsFeed(
            publisher="Feuerwehr Vienenburg",
            url="https://feuerwehr-vienenburg.de/feed/",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Feuerwehr Hahndorf", url="https://feuerwehr-hahndorf.de/feed/"
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Feuerwehr Wiedelah",
            url="https://www.feuerwehr-wiedelah.de/rss/blog",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Feuerwehr Jerstedt",
            url="http://www.ffw-jerstedt.de/index.php/einsaetze?format=feed&type=rss",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Feuerwehr Oker",
            url="https://www.feuerwehr-oker.de/index.php/aktuelles/einsaetze/einsatzberichte?format=feed&type=rss",
        )
    )
    news_feeds.append(
        NewsFeed(
            publisher="Bevölkerungsschutz",
            url="https://warnung.bund.de/bbk.mowas/rss/031530000000.xml",
        )
    )

    for news_feed in news_feeds:
        scrape_feed(
            now,
            min_date,
            news_feed,
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


def scrape_feed(now, min_date, news_feed: NewsFeed):
    try:
        url = news_feed.url
        publisher_name = news_feed.publisher
        title_filter = news_feed.title_filter
        title_sub_pattern = news_feed.title_sub_pattern
        title_sub_repl = news_feed.title_sub_repl

        print(url)
        channel = feedparser.parse(url)
        entry_ids = list()

        title_filter_regex = re.compile(title_filter) if title_filter else None
        title_sub_pattern_regex = (
            re.compile(title_sub_pattern) if title_sub_pattern else None
        )

        for entry in channel.entries:

            if (
                "published" not in entry or "title" not in entry or "link" not in entry
            ):  # pragma: no cover
                continue

            title = entry.title

            if title_filter_regex and not title_filter_regex.match(title):
                continue

            if title_sub_pattern_regex:
                title = title_sub_pattern_regex.sub(title_sub_repl, title)

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
