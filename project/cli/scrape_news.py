import datetime
import re
from pprint import pprint

import feedparser
from dateutil import parser
from sqlalchemy.sql import and_, not_

from project import db
from project.dateutils import get_now
from project.models import NewsFeed, NewsItem


def scrape():
    now = get_now()
    min_date = now - datetime.timedelta(days=14)

    news_feeds = NewsFeed.query.all()
    for news_feed in news_feeds:
        scrape_feed(
            now,
            min_date,
            news_feed,
        )

    delete_old_items(min_date)


def upsert_news_item(news_feed: NewsFeed, entry_id, title, link, published, fetched):
    item = NewsItem.query.filter_by(
        news_feed_id=news_feed.id, source_id=entry_id
    ).first()
    item_did_exist = False
    if item is None:
        item = NewsItem(news_feed_id=news_feed.id, source_id=entry_id)
    else:
        item_did_exist = True

    item.content = title
    item.link_url = link
    item.published = published
    item.fetched = fetched

    if not item_did_exist:
        db.session.add(item)


def scrape_feed(now, min_date, news_feed: NewsFeed):
    try:
        url = news_feed.url
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

            upsert_news_item(news_feed, entry_id, title, entry.link, published, now)
            entry_ids.append(entry_id)

        # Delete entries that are not part of the feed anymore
        NewsItem.query.filter(
            and_(
                NewsItem.news_feed_id == news_feed.id,
                not_(NewsItem.source_id.in_(entry_ids)),
            )
        ).delete(synchronize_session=False)

    except Exception as e:  # pragma: no cover
        pprint(e)
    finally:
        db.session.commit()


def delete_old_items(min_date):
    NewsItem.query.filter(NewsItem.published <= min_date).delete()
    db.session.commit()
