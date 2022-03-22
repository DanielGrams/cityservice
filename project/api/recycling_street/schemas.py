from flask_security import current_user
from marshmallow import fields

from project.api import marshmallow
from project.api.recycling_event.schemas import (
    RecyclingEventListRequestSchema,
    RecyclingEventListResponseSchema,
)
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


class RecyclingStreetCurrentUserMixin(object):
    is_favored = fields.Method(
        "get_is_favored",
        metadata={
            "description": "True, if recycling street is favored by current user"
        },
    )

    def get_is_favored(self, event):
        if not current_user or not current_user.is_authenticated:
            return False

        from project.services.user import has_user_recycling_street

        return has_user_recycling_street(current_user.id, event.id)


class RecyclingStreetSchema(
    RecyclingStreetIdSchema,
    RecyclingStreetBaseSchemaMixin,
    RecyclingStreetCurrentUserMixin,
):
    pass


class RecyclingStreetRefSchema(RecyclingStreetIdSchema):
    name = marshmallow.auto_field()


class PlaceRecyclingStreetListRequestSchema(PaginationRequestSchema):
    keyword = fields.Str()


class RecyclingStreetListItemSchema(
    RecyclingStreetRefSchema, RecyclingStreetCurrentUserMixin
):
    pass


class PlaceRecyclingStreetListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(RecyclingStreetListItemSchema),
        metadata={"description": "Recycling streets"},
    )


class UserRecyclingStreetListRequestSchema(PaginationRequestSchema):
    pass


class UserRecyclingStreetListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(RecyclingStreetRefSchema),
        metadata={"description": "Recycling streets"},
    )


class RecyclingStreetEventListRequestSchema(RecyclingEventListRequestSchema):
    pass


class RecyclingStreetEventListResponseSchema(RecyclingEventListResponseSchema):
    pass
