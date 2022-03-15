from marshmallow import fields

from project.api import marshmallow
from project.api.schemas import (
    IdSchemaMixin,
    PaginationRequestSchema,
    PaginationResponseSchema,
    SQLAlchemyBaseSchema,
)
from project.models import RecyclingStreet


class RecyclingStreetModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingStreet
        load_instance = True


class RecyclingStreetIdSchema(RecyclingStreetModelSchema, IdSchemaMixin):
    pass


class RecyclingStreetBaseSchemaMixin(object):
    name = marshmallow.auto_field()


class RecyclingStreetSchema(RecyclingStreetIdSchema, RecyclingStreetBaseSchemaMixin):
    name = marshmallow.auto_field()


class RecyclingStreetRefSchema(RecyclingStreetIdSchema):
    name = marshmallow.auto_field()


class UserRecyclingStreetListRequestSchema(PaginationRequestSchema):
    pass


class UserRecyclingStreetListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(RecyclingStreetRefSchema),
        metadata={"description": "Recycling streets"},
    )
