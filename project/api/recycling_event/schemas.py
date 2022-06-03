from flask import url_for
from marshmallow import fields

from project.api import marshmallow
from project.api.fields import CustomDateTimeField
from project.api.place.schemas import PlaceRefSchema
from project.api.recycling_street.schemas import RecyclingStreetRefSchema
from project.api.schemas import (
    IdSchemaMixin,
    PaginationRequestSchema,
    PaginationResponseSchema,
    SQLAlchemyBaseSchema,
)
from project.models import RecyclingEvent


class RecyclingEventModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingEvent
        load_instance = True


class RecyclingEventIdSchema(RecyclingEventModelSchema, IdSchemaMixin):
    pass


class RecyclingEventBaseSchemaMixin(object):
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


class LegacyRecyclingEventSchema(
    RecyclingEventModelSchema, RecyclingEventBaseSchemaMixin
):
    pass


class RecyclingEventSchema(RecyclingEventIdSchema, RecyclingEventBaseSchemaMixin):
    pass


class RecyclingEventListRequestSchema(PaginationRequestSchema):
    all = fields.Boolean(
        required=False,
        default=False,
    )


class RecyclingEventListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(RecyclingEventSchema), metadata={"description": "Events"}
    )


class UserRecyclingEventListRequestSchema(PaginationRequestSchema):
    pass


class UserRecyclingEventListItemSchema(
    RecyclingEventSchema,
):
    street = fields.Nested(RecyclingStreetRefSchema)
    place = fields.Nested(PlaceRefSchema, attribute="street.place")


class UserRecyclingEventListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(UserRecyclingEventListItemSchema),
        metadata={"description": "Recycling events"},
    )


class RecyclingStreetEventListRequestSchema(RecyclingEventListRequestSchema):
    pass


class RecyclingStreetEventListResponseSchema(RecyclingEventListResponseSchema):
    pass
