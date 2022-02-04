class ModelSeeder(object):
    def __init__(self, db):
        self._db = db

    def create_news_item(self, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import NewsItem

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
        return news_item.id
