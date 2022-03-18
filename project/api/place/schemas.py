from flask_security import current_user
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


class PlaceCurrentUserMixin(object):
    is_favored = fields.Method(
        "get_is_favored",
        metadata={"description": "True, if place is favored by current user"},
    )

    def get_is_favored(self, event):
        if not current_user or not current_user.is_authenticated:  # pragma: no cover
            return False

        from project.services.user import has_user_place

        return has_user_place(current_user.id, event.id)


class PlaceSchema(PlaceIdSchema, PlaceBaseSchemaMixin, PlaceCurrentUserMixin):
    pass


class PlaceRefSchema(PlaceIdSchema):
    name = marshmallow.auto_field()


class PlaceListRequestSchema(PaginationRequestSchema):
    keyword = fields.Str()


class PlaceListItemSchema(PlaceRefSchema, PlaceCurrentUserMixin):
    pass


class PlaceListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(PlaceListItemSchema), metadata={"description": "Places"}
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
