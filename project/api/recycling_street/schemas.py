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
from project.models import RecyclingStreet, RecyclingStreetsUsers


class RecyclingStreetModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingStreet
        load_instance = True


class RecyclingStreetIdSchema(RecyclingStreetModelSchema, IdSchemaMixin):
    pass


class RecyclingStreetBaseSchemaMixin(object):
    name = marshmallow.auto_field()


class RecyclingStreetCurrentUserFavoriteMixin(object):
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


class RecyclingStreetCurrentUserNotificationsMixin(object):
    notifications_active = fields.Method(
        "get_notifications_active",
        metadata={"description": "True, if notifications are active for current user"},
    )

    def get_notifications_active(self, event):
        if not current_user or not current_user.is_authenticated:
            return False

        from project.services.user import get_user_recycling_street_notifications_active

        return get_user_recycling_street_notifications_active(current_user.id, event.id)


class RecyclingStreetSchema(
    RecyclingStreetIdSchema,
    RecyclingStreetBaseSchemaMixin,
    RecyclingStreetCurrentUserFavoriteMixin,
    RecyclingStreetCurrentUserNotificationsMixin,
):
    pass


class RecyclingStreetRefSchema(RecyclingStreetIdSchema):
    name = marshmallow.auto_field()


class PlaceRecyclingStreetListRequestSchema(PaginationRequestSchema):
    keyword = fields.Str()


class PlaceRecyclingStreetListItemSchema(
    RecyclingStreetRefSchema,
    RecyclingStreetCurrentUserFavoriteMixin,
    RecyclingStreetCurrentUserNotificationsMixin,
):
    pass


class PlaceRecyclingStreetListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(PlaceRecyclingStreetListItemSchema),
        metadata={"description": "Recycling streets"},
    )


class UserRecyclingStreetListRequestSchema(PaginationRequestSchema):
    pass


class UserRecyclingStreetListItemSchema(
    RecyclingStreetRefSchema,
    RecyclingStreetCurrentUserNotificationsMixin,
):
    pass


class UserRecyclingStreetListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(UserRecyclingStreetListItemSchema),
        metadata={"description": "Recycling streets"},
    )


class RecyclingStreetEventListRequestSchema(RecyclingEventListRequestSchema):
    pass


class RecyclingStreetEventListResponseSchema(RecyclingEventListResponseSchema):
    pass


class UserRecyclingStreetModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingStreetsUsers
        load_instance = True


class UserRecyclingStreetBaseSchemaMixin(object):
    pass


class UserRecyclingStreetWriteSchemaMixin(object):
    notifications_active = marshmallow.auto_field(
        required=False,
        default=False,
    )


class UserRecyclingStreetPatchRequestSchema(
    UserRecyclingStreetModelSchema,
    UserRecyclingStreetBaseSchemaMixin,
    UserRecyclingStreetWriteSchemaMixin,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_patch_schema()
