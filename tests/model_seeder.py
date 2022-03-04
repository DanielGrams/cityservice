class ModelSeeder(object):
    def __init__(self, db):
        self._db = db

    def create_news_item(self, news_feed_id: int, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import NewsItem

        news_item = NewsItem(
            news_feed_id=news_feed_id,
            content="Ein Einsatz war",
            link_url="https://example.com",
            published=create_berlin_date(2050, 1, 1, 12),
        )
        news_item.__dict__.update(kwargs)

        self._db.session.add(news_item)
        self._db.session.commit()
        return news_item.id

    def create_news_feed(self, **kwargs) -> int:
        from project.models import NewsFeed, NewsFeedType

        news_feed = NewsFeed(
            publisher="Feuerwehr",
            feed_type=NewsFeedType.fire_department,
            url="https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
        )
        news_feed.__dict__.update(kwargs)

        self._db.session.add(news_feed)
        self._db.session.commit()
        return news_feed.id

    def create_weather_warning(self, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import WeatherWarning

        weather_warning = WeatherWarning(
            headline="Amtliche WARNUNG vor FROST",
            content="Es tritt mäßiger Frost zwischen -3 °C und -6 °C auf.",
            start=create_berlin_date(2050, 1, 1, 14),
            end=create_berlin_date(2050, 1, 1, 20),
            published=create_berlin_date(2050, 1, 1, 13),
        )
        weather_warning.__dict__.update(kwargs)

        self._db.session.add(weather_warning)
        self._db.session.commit()
        return weather_warning.id
