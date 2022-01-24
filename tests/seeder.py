class Seeder(object):
    def __init__(self, app, db, utils):
        self._app = app
        self._db = db
        self._utils = utils

    def create_news_item(self, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import NewsItem

        with self._app.app_context():
            news_item = NewsItem()
            news_item.publisher_name = (
                kwargs["publisher_name"] if "publisher_name" in kwargs else "Feuerwehr"
            )
            news_item.content = (
                kwargs["content"] if "content" in kwargs else "Ein Einsatz war"
            )
            news_item.link_url = (
                kwargs["link_url"] if "link_url" in kwargs else "https://example.com"
            )
            news_item.published = (
                kwargs["published"]
                if "published" in kwargs
                else create_berlin_date(2050, 1, 1, 12)
            )

            self._db.session.add(news_item)
            self._db.session.commit()
            news_item_id = news_item.id

        return news_item_id

    def create_recycling_street(self, **kwargs) -> int:
        from project.models import RecyclingStreet

        with self._app.app_context():
            recycling_street = RecyclingStreet()
            recycling_street.town_id = (
                kwargs["town_id"] if "town_id" in kwargs else "38640"
            )
            recycling_street.name = (
                kwargs["name"] if "name" in kwargs else "Schreiberstraße"
            )

            self._db.session.add(recycling_street)
            self._db.session.commit()
            recycling_street_id = recycling_street.id

        return recycling_street_id

    def create_recycling_event(self, street_id: int, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import RecyclingEvent

        with self._app.app_context():
            recycling_event = RecyclingEvent()
            recycling_event.street_id = street_id
            recycling_event.category = (
                kwargs["category"] if "category" in kwargs else "Biotonne"
            )
            recycling_event.date = (
                kwargs["date"]
                if "date" in kwargs
                else create_berlin_date(2050, 1, 1, 12)
            )

            self._db.session.add(recycling_event)
            self._db.session.commit()
            recycling_event_id = recycling_event.id

        return recycling_event_id
