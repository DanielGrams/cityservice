from flask import url_for
from marshmallow import fields

from project.api import marshmallow
from project.api.fields import CustomDateTimeField
from project.api.schemas import SQLAlchemyBaseSchema
from project.models import RecyclingEvent


class RecyclingEventSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingEvent
        load_instance = True

    category = marshmallow.auto_field()
    date = CustomDateTimeField()
    category_icon_url = fields.Method("get_category_icon_url")

    def get_category_icon_url(self, item):  # pragma: no cover
        if item.category == "Baum- und Strauchschnitt":
            return url_for("serve_file_in_dir", path="1.5.png", _external=True)
        elif item.category == "Biotonne":
            return url_for("serve_file_in_dir", path="1.4.png", _external=True)
        elif item.category == "Blaue Tonne":
            return url_for("serve_file_in_dir", path="1.3.png", _external=True)
        elif item.category == "Gelber Sack":
            return url_for("serve_file_in_dir", path="1.2.png", _external=True)
        elif item.category == "Restmülltonne":
            return url_for("serve_file_in_dir", path="1.1.png", _external=True)
        elif item.category == "Weihnachtsbäume":
            return url_for("serve_file_in_dir", path="1.6.png", _external=True)
        elif item.category == "Wertstofftonne danach":
            return url_for("serve_file_in_dir", path="2523.1.png", _external=True)
