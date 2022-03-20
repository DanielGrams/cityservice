from flask import url_for
from marshmallow import fields

from project.api import marshmallow
from project.api.fields import CustomDateTimeField
from project.api.news_feed.schemas import NewsFeedRefSchema
from project.api.schemas import (
    IdSchemaMixin,
    PaginationRequestSchema,
    PaginationResponseSchema,
    SQLAlchemyBaseSchema,
)
from project.models import NewsFeedType, NewsItem


class NewsItemModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = NewsItem
        load_instance = True


class NewsItemIdSchema(NewsItemModelSchema, IdSchemaMixin):
    pass


class NewsItemBaseSchemaMixin(object):
    content = marshmallow.auto_field()
    link_url = marshmallow.auto_field()
    published = CustomDateTimeField()
    news_feed = fields.Nested(NewsFeedRefSchema)
    publisher_icon_url = fields.Method(
        "get_publisher_icon_url",
    )

    def get_publisher_icon_url(self, news_item: NewsItem):
        return get_publisher_icon_url_for_news_item(news_item)


class NewsItemSchema(NewsItemIdSchema, NewsItemBaseSchemaMixin):
    pass


class NewsItemListRequestSchema(PaginationRequestSchema):
    pass


class NewsItemListItemSchema(NewsItemIdSchema, NewsItemBaseSchemaMixin):
    pass


class NewsItemListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(NewsItemListItemSchema), metadata={"description": "News items"}
    )


class LegacyNewsItemSchema(marshmallow.Schema):
    publisher_name = fields.Str()
    content = fields.Str()
    link_url = fields.Str()
    published = CustomDateTimeField()
    publisher_icon_url = fields.Str()


def get_publisher_icon_url_for_news_item(news_item: NewsItem):
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
