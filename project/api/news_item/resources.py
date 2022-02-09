from flask_apispec import doc, marshal_with

from project.api import add_api_resource
from project.api.news_item.schemas import NewsItemSchema
from project.api.resources import BaseResource
from project.models import NewsItem


class NewsItemListResource(BaseResource):
    @doc(summary="List news items", tags=["News"])
    @marshal_with(NewsItemSchema(many=True))
    def get(self):
        items = NewsItem.query.order_by(NewsItem.published.desc()).all()
        return items


add_api_resource(NewsItemListResource, "/newsitems", "api_news_item_list")
