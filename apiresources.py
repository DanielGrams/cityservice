from app import marshmallow
from models import NewsItem
from flask_restful import Resource

class NewsItemSchema(marshmallow.Schema):
    class Meta:
        fields = ("publisher_name", "publisher_icon_url", "content", "link_url", "published")

news_item_schema = NewsItemSchema()
news_items_schema = NewsItemSchema(many=True)

class NewsItemList(Resource):
    def get(self):
        items =  NewsItem.query.order_by(NewsItem.published.desc()).all()
        return news_items_schema.dump(items)
