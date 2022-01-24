import flask
from flask_apispec import doc, marshal_with

from project.api import add_api_resource
from project.api.news_item.schemas import NewsItemSchema, news_items_schema
from project.api.resources import BaseResource
from project.models import NewsItem


class NewsItemList(BaseResource):
    @doc(summary="List news items", tags=["News"])
    @marshal_with(NewsItemSchema(many=True))
    def get(self):
        items = NewsItem.query.order_by(NewsItem.published.desc()).all()

        for item in items:  # pragma: no cover
            if item.publisher_name == "Stadt Goslar":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="city-solid.png", _external=True
                )
            elif item.publisher_name == "Landkreis Goslar":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="landmark-solid.png", _external=True
                )
            elif item.publisher_name == "KWB Goslar":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="truck-solid.png", _external=True
                )
            elif item.publisher_name == "Polizei Goslar":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="taxi-solid.png", _external=True
                )
            elif item.publisher_name == "Stadtbibliothek Goslar":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="book-solid.png", _external=True
                )
            elif item.publisher_name == "Mach mit!":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="users-solid.png", _external=True
                )
            elif item.publisher_name.startswith("Feuerwehr"):
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="taxi-solid-red.png", _external=True
                )
            elif item.publisher_name == "Bevölkerungsschutz":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="warning-solid.png", _external=True
                )
            elif item.publisher_name == "Deutscher Wetterdienst":
                item.publisher_icon_url = flask.url_for(
                    "serve_file_in_dir", path="warning-solid.png", _external=True
                )

        data = news_items_schema.dump(items)
        return data


add_api_resource(NewsItemList, "/newsitems", "api_news_item_list")
