class ModelSeeder(object):
    def __init__(self, db):
        self._db = db

    def create_user(
        self, email="test@test.de", password="MeinPasswortIstDasBeste", admin=False
    ):
        from flask_security.confirmable import confirm_user

        from project.services.user import (
            add_admin_roles_to_user,
            create_user,
            find_user_by_email,
        )

        user = find_user_by_email(email)

        if user is None:
            user = create_user(email, password)
            confirm_user(user)

        if admin:
            add_admin_roles_to_user(email)

        self._db.session.commit()
        return user.id

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

    def create_place(self, **kwargs) -> int:
        from project.models import Place

        place = Place(
            name="Goslar",
            recycling_ids="2523.1,2523.8,2523.10",
            weather_warning_name="Stadt Goslar",
        )
        place.__dict__.update(kwargs)

        self._db.session.add(place)
        self._db.session.commit()
        return place.id

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

    def create_recycling_street(self, **kwargs) -> int:
        from project.models import RecyclingStreet

        recycling_street = RecyclingStreet(
            town_id="2523.1", name="Schreiberstraße, Goslar"
        )
        recycling_street.__dict__.update(kwargs)

        self._db.session.add(recycling_street)
        self._db.session.commit()
        return recycling_street.id

    def create_recycling_event(self, street_id: int, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import RecyclingEvent

        recycling_event = RecyclingEvent(
            street_id=street_id,
            category="Biotonne",
            date=create_berlin_date(2050, 1, 1, 12),
        )
        recycling_event.__dict__.update(kwargs)

        self._db.session.add(recycling_event)
        self._db.session.commit()
        return recycling_event.id

    def add_user_recycling_street(self, user_id, recyclingstreet_id):
        from project.services.user import add_user_recycling_street

        if add_user_recycling_street(user_id, recyclingstreet_id):
            self._db.session.commit()

    def remove_user_recycling_street(self, user_id, recyclingstreet_id):
        from project.services.user import remove_user_recycling_street

        if remove_user_recycling_street(user_id, recyclingstreet_id):
            self._db.session.commit()

    def add_user_place(self, user_id, place_id):
        from project.services.user import add_user_place

        if add_user_place(user_id, place_id):
            self._db.session.commit()

    def remove_user_place(self, user_id, place_id):
        from project.services.user import remove_user_place

        if remove_user_place(user_id, place_id):
            self._db.session.commit()

    def create_common_scenario(self):
        import datetime

        from project.dateutils import create_berlin_date, get_today
        from project.models import NewsFeed, NewsFeedType, Place

        today = get_today()
        yesterday = today + datetime.timedelta(days=-1)

        # User
        user_id = self.create_user()

        # Places
        goslar_id = self.create_place(
            name="Goslar",
            recycling_ids="2523.1,2523.8,2523.10",
            weather_warning_name="Stadt Goslar",
        )

        self.create_place(
            name="Bad Harzburg",
            recycling_ids="2523.2",
            weather_warning_name="Stadt Bad Harzburg",
        )
        self.create_place(
            name="Braunlage",
            recycling_ids="2523.3",
            weather_warning_name="Stadt Braunlage",
        )
        self.create_place(
            name="Clausthal-Zellerfeld",
            recycling_ids="2523.4",
            weather_warning_name="Gemeinde Clausthal-Zellerfeld",
        )
        langelsheim_id = self.create_place(
            name="Langelsheim",
            recycling_ids="2523.5,2523.7",
            weather_warning_name="Stadt Langelsheim",
        )
        self.create_place(
            name="Liebenburg",
            recycling_ids="2523.6",
            weather_warning_name="Gemeinde Liebenburg",
        )
        self.create_place(
            name="Seesen",
            recycling_ids="2523.9",
            weather_warning_name="Stadt Seesen",
        )

        # News feeds
        places = Place.query.all()
        for place in places:
            self.create_news_feed(
                place_id=place.id,
                publisher="Stadt",
                feed_type=NewsFeedType.city,
                url="https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="Landkreis",
                feed_type=NewsFeedType.district,
                url="https://www.landkreis-goslar.de/media/rss/Pressemitteilung.xml",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="KWB",
                feed_type=NewsFeedType.district,
                url="https://www.kwb-goslar.de/media/rss/Pressemitteilungen.xml",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="Polizei",
                feed_type=NewsFeedType.police,
                url="http://www.presseportal.de/rss/dienststelle_56518.rss2",
                title_filter=".*(Goslar|Vienenburg).*",
                title_sub_pattern="POL-GS:",
                title_sub_repl="",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="Stadtbibliothek",
                feed_type=NewsFeedType.city,
                url="https://stadtbibliothek.goslar.de/stadtbibliothek/aktuelles?format=feed&type=rss",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="Mach mit!",
                feed_type=NewsFeedType.citizen_participation,
                url="https://machmit.goslar.de/category/machmit-prozess/feed",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="Feuerwehr",
                feed_type=NewsFeedType.fire_department,
                url="https://feuerwehr-goslar.de/feed/",
            )
            self.create_news_feed(
                place_id=place.id,
                publisher="Bevölkerungsschutz",
                feed_type=NewsFeedType.civil_protection,
                url="https://warnung.bund.de/bbk.mowas/rss/031530000000.xml",
            )

        # News items
        news_feeds = NewsFeed.query.all()
        for news_feed in news_feeds:
            self.create_news_item(
                news_feed.id,
                content="Es gibt etwas Neues!",
                published=today,
            )
            self.create_news_item(
                news_feed.id,
                content="Es wird etwas Neues geben!",
                published=yesterday,
            )

        # Recycling
        begin_of_year = create_berlin_date(today.year, 1, 1)
        street_names = [
            "Ortsteil - Hahndorf",
            "Ortsteil - Hahnenklee-Bockswiese",
            "Ortsteil - Jerstedt",
            "Stadtteil - Georgenberg",
            "Stadtteil - Kattenberg",
            "Am Marienbad",
            "An der Gose",
            "Brieger Eck",
            "Christian-von-Dohm-Platz",
            "Domplatz",
            "Frankenberger Straße",
            "Schreiberstraße",
        ]
        for name in street_names:
            street_name = f"{name}, Goslar"
            street_id = self.create_recycling_street(
                place_id=goslar_id, town_id="2523.1", name=street_name
            )

            categories = ["Biotonne", "Blaue Tonne", "Gelber Sack", "Restmülltonne"]
            len_categories = len(categories)
            offset = 0
            index = 0

            while offset < 365:
                date = begin_of_year + datetime.timedelta(days=offset)
                category = categories[index % len_categories]
                self.create_recycling_event(street_id, category=category, date=date)
                index = index + 1
                offset = offset + 2

        # Weather
        for place in places:
            self.create_weather_warning(
                place_id=place.id,
                headline="Amtliche WARNUNG vor FROST",
                content="Es tritt mäßiger Frost zwischen -3 °C und -6 °C auf.",
                start=create_berlin_date(today.year, today.month, today.day, 14),
                end=create_berlin_date(today.year, today.month, today.day, 20),
                published=today,
            )
            self.create_weather_warning(
                place_id=place.id,
                headline="Amtliche WARNUNG vor NEBEL",
                content="Es tritt gebietsweise Nebel mit Sichtweiten unter 150 Metern auf.",
                start=create_berlin_date(today.year, today.month, today.day, 18),
                end=create_berlin_date(today.year, today.month, today.day, 22),
                published=today,
            )

        # User
        self.add_user_place(user_id, goslar_id)
        self.add_user_place(user_id, langelsheim_id)
        self.add_user_recycling_street(user_id, street_id)
