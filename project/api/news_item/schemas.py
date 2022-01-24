from project.api.schemas import SQLAlchemyBaseSchema
from project.models import NewsItem


class NewsItemSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = NewsItem
        fields = (
            "publisher_name",
            "content",
            "link_url",
            "published",
            "publisher_icon_url",
        )


news_item_schema = NewsItemSchema()
news_items_schema = NewsItemSchema(many=True)
