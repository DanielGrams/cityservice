from app import marshmallow, app
from models import NewsItem, RecyclingStreet, RecyclingEvent
import flask
from flask_restful import Resource
from flask_marshmallow import Marshmallow, fields
import os

class NewsItemSchema(marshmallow.Schema):
    class Meta:
        fields = ("publisher_name", "content", "link_url", "published", "publisher_icon_url")

news_item_schema = NewsItemSchema()
news_items_schema = NewsItemSchema(many=True)

class RecyclingStreetSchema(marshmallow.Schema):
    class Meta:
        fields = ("id", "name")

recycling_street_schema = RecyclingStreetSchema()
recycling_streets_schema = RecyclingStreetSchema(many=True)

class RecyclingEventSchema(marshmallow.Schema):
    class Meta:
        fields = ("date", "category")

recycling_event_schema = RecyclingEventSchema()
recycling_events_schema = RecyclingEventSchema(many=True)

class NewsItemList(Resource):
    def get(self):
        items =  NewsItem.query.order_by(NewsItem.published.desc()).all()

        for item in items:
            if item.publisher_name == "Stadt Goslar":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="city-solid.png", _external=True)
            elif item.publisher_name == "Landkreis Goslar":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="landmark-solid.png", _external=True)
            elif item.publisher_name == "KWB Goslar":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="truck-solid.png", _external=True)
            elif item.publisher_name == "Polizei Goslar":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="taxi-solid.png", _external=True)
            elif item.publisher_name == "Stadtbibliothek Goslar":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="book-solid.png", _external=True)

        return news_items_schema.dump(items)

class RecyclingStreetList(Resource):
    def get(self):
        items =  RecyclingStreet.query.order_by(RecyclingStreet.name).all()
        return recycling_streets_schema.dump(items)

class RecyclingEventList(Resource):
    def get(self, street_id):
        RecyclingStreet.query.filter_by(id = street_id).first_or_404(description='Die Straße ist nicht vorhanden.')
        items =  RecyclingEvent.query.filter_by(street_id = street_id).order_by(RecyclingEvent.date).all()
        return recycling_events_schema.dump(items)
