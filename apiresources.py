from app import marshmallow, app, api
from models import NewsItem, RecyclingStreet, RecyclingEvent
import flask
import flask_restful
from flask_marshmallow import Marshmallow, fields
import os
import datetime
import pytz
from sqlalchemy import and_
from functools import wraps
import json
from pprint import pprint
from hashlib import md5

#
# Schemes
#

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
        fields = ("date", "category", "category_icon_url")

recycling_event_schema = RecyclingEventSchema()
recycling_events_schema = RecyclingEventSchema(many=True)

#
# Resources
#

def etag_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        dump = json.dumps(data, sort_keys=True)
        response = flask.make_response(dump)
        response.add_etag()
        return response.make_conditional(flask.request)
    return wrapper


class Resource(flask_restful.Resource):
    method_decorators = [etag_cache]   # applies to all inherited resources

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
            elif item.publisher_name == "Mach mit!":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="users-solid.png", _external=True)
            elif item.publisher_name == "Feuerwehr Goslar":
                item.publisher_icon_url = flask.url_for("serve_file_in_dir", path="taxi-solid-red.png", _external=True)

        data = news_items_schema.dump(items)
        return data


class RecyclingStreetList(Resource):
    def get(self):
        items =  RecyclingStreet.query.all()
        sorted_items = sorted(items, key=lambda item: (not item.name.startswith('Ortsteil') and not item.name.startswith('Stadtteil'), item.name))
        return recycling_streets_schema.dump(sorted_items)

class RecyclingEventList(Resource):
    def get(self, street_id):
        RecyclingStreet.query.filter_by(id = street_id).first_or_404(description='Die Straße ist nicht vorhanden.')

        if 'all' in flask.request.args:
            items =  RecyclingEvent.query.filter(RecyclingEvent.street_id == street_id).order_by(RecyclingEvent.date).all()
        else:
            now = datetime.datetime.now(tz=pytz.timezone('Europe/Berlin'))
            today = datetime.datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)
            items =  RecyclingEvent.query.filter(and_(RecyclingEvent.street_id == street_id, RecyclingEvent.date >= today)).order_by(RecyclingEvent.date).all()

        for item in items:
            if item.category == "Baum- und Strauchschnitt":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="1.5.png", _external=True)
            elif item.category == "Biotonne":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="1.4.png", _external=True)
            elif item.category == "Blaue Tonne":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="1.3.png", _external=True)
            elif item.category == "Gelber Sack":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="1.2.png", _external=True)
            elif item.category == "Restmülltonne":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="1.1.png", _external=True)
            elif item.category == "Weihnachtsbäume":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="1.6.png", _external=True)
            elif item.category == "Wertstofftonne danach":
                item.category_icon_url = flask.url_for("serve_file_in_dir", path="2523.1.png", _external=True)

        return recycling_events_schema.dump(items)
