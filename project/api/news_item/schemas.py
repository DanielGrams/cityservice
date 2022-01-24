from flask import url_for
from marshmallow import fields

from project.api import marshmallow
from project.api.fields import CustomDateTimeField
from project.api.schemas import SQLAlchemyBaseSchema
from project.models import NewsItem


class NewsItemSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = NewsItem
        load_instance = True

    publisher_name = marshmallow.auto_field()
    content = marshmallow.auto_field()
    link_url = marshmallow.auto_field()
    published = CustomDateTimeField()
    publisher_icon_url = fields.Method("get_publisher_icon_url")

    def get_publisher_icon_url(self, item):  # pragma: no cover
        if item.publisher_name == "Stadt Goslar":
            return url_for("serve_file_in_dir", path="city-solid.png", _external=True)
        elif item.publisher_name == "Landkreis Goslar":
            return url_for(
                "serve_file_in_dir", path="landmark-solid.png", _external=True
            )
        elif item.publisher_name == "KWB Goslar":
            return url_for("serve_file_in_dir", path="truck-solid.png", _external=True)
        elif item.publisher_name == "Polizei Goslar":
            return url_for("serve_file_in_dir", path="taxi-solid.png", _external=True)
        elif item.publisher_name == "Stadtbibliothek Goslar":
            return url_for("serve_file_in_dir", path="book-solid.png", _external=True)
        elif item.publisher_name == "Mach mit!":
            return url_for("serve_file_in_dir", path="users-solid.png", _external=True)
        elif item.publisher_name.startswith("Feuerwehr"):
            return url_for(
                "serve_file_in_dir", path="taxi-solid-red.png", _external=True
            )
        elif item.publisher_name == "Bevölkerungsschutz":
            return url_for(
                "serve_file_in_dir", path="warning-solid.png", _external=True
            )
        elif item.publisher_name == "Deutscher Wetterdienst":
            return url_for(
                "serve_file_in_dir", path="warning-solid.png", _external=True
            )
