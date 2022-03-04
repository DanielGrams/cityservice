from flask import url_for
from flask_apispec import doc, marshal_with

from project.api import add_api_resource
from project.api.news_item.schemas import NewsItemSchema
from project.api.resources import BaseResource
from project.models import NewsFeedType, NewsItem, WeatherWarning


class NewsItemListResource(BaseResource):
    @doc(summary="List news items", tags=["News"])
    @marshal_with(NewsItemSchema(many=True))
    def get(self):
        items = list()

        news_items = NewsItem.query.all()
        for news_item in news_items:
            item = {
                "publisher_name": news_item.news_feed.publisher,
                "content": news_item.content,
                "link_url": news_item.link_url,
                "published": news_item.published,
                "publisher_icon_url": self.get_publisher_icon_url_for_news_item(
                    news_item
                ),
            }
            items.append(item)

        weather_warnings = WeatherWarning.query.all()
        number_of_weather_warnings = len(weather_warnings)
        if number_of_weather_warnings > 0:
            weather_warning = weather_warnings[0]

            content = weather_warning.headline
            if number_of_weather_warnings == 2:
                content = f"{content} und eine weitere Warnung"
            elif number_of_weather_warnings > 2:
                content = (
                    f"{content} und {number_of_weather_warnings - 1} weitere Warnungen"
                )

            item = {
                "publisher_name": "Deutscher Wetterdienst",
                "content": content,
                "link_url": "https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html?ort=Goslar",
                "published": weather_warning.published,
                "publisher_icon_url": url_for(
                    "serve_file_in_dir", path="warning-solid.png", _external=True
                ),
            }
            items.append(item)

        sorted_items = sorted(items, key=lambda i: i["published"], reverse=True)
        return sorted_items

    def get_publisher_icon_url_for_news_item(self, news_item: NewsItem):
        mapping = {
            NewsFeedType.unknown: None,
            NewsFeedType.city: "city-solid.png",
            NewsFeedType.district: "landmark-solid.png",
            NewsFeedType.police: "taxi-solid.png",
            NewsFeedType.fire_department: "taxi-solid-red.png",
            NewsFeedType.culture: "book-solid.png",
            NewsFeedType.citizen_participation: "users-solid.png",
            NewsFeedType.civil_protection: "warning-solid.png",
        }
        path = mapping.get(news_item.news_feed.feed_type, None)

        if not path:  # pragma: no cover
            return None

        return url_for("serve_file_in_dir", path=path, _external=True)


add_api_resource(NewsItemListResource, "/newsitems", "api_news_item_list")
