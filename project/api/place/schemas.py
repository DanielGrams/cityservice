from marshmallow import fields, validate

from project.api import marshmallow
from project.api.schemas import (
    IdSchemaMixin,
    PaginationRequestSchema,
    PaginationResponseSchema,
    SQLAlchemyBaseSchema,
    TrackableSchemaMixin,
    WriteIdSchemaMixin,
)
from project.models import Place


class PlaceModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = Place
        load_instance = True


class PlaceIdSchema(PlaceModelSchema, IdSchemaMixin):
    pass


class PlaceWriteIdSchema(PlaceModelSchema, WriteIdSchemaMixin):
    pass


class PlaceBaseSchemaMixin(TrackableSchemaMixin):
    name = marshmallow.auto_field(
        required=True, validate=validate.Length(min=3, max=255)
    )
    recycling_ids = marshmallow.auto_field(validate=[validate.Length(max=255)])
    weather_warning_name = marshmallow.auto_field(validate=[validate.Length(max=255)])


class PlaceSchema(PlaceIdSchema, PlaceBaseSchemaMixin):
    pass


class PlaceRefSchema(PlaceIdSchema):
    name = marshmallow.auto_field()


class PlaceListRequestSchema(PaginationRequestSchema):
    keyword = fields.Str()


class PlaceListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(PlaceRefSchema), metadata={"description": "Places"}
    )


class PlacePostRequestSchema(PlaceModelSchema, PlaceBaseSchemaMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_post_schema()


class PlacePatchRequestSchema(PlaceModelSchema, PlaceBaseSchemaMixin):
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        self.make_patch_schema()


class UserPlaceListRequestSchema(PaginationRequestSchema):
    pass


class UserPlaceListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(PlaceRefSchema),
        metadata={"description": "Places"},
    )
