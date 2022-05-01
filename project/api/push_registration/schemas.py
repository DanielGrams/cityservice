from marshmallow import fields, validate
from marshmallow_enum import EnumField

from project.api import marshmallow
from project.api.schemas import (
    IdSchemaMixin,
    PaginationRequestSchema,
    PaginationResponseSchema,
    SQLAlchemyBaseSchema,
    TrackableSchemaMixin,
    WriteIdSchemaMixin,
)
from project.models import PushPlatform, PushRegistration


class PushRegistrationModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = PushRegistration
        load_instance = True


class PushRegistrationIdSchema(PushRegistrationModelSchema, IdSchemaMixin):
    pass


class PushRegistrationWriteIdSchema(PushRegistrationModelSchema, WriteIdSchemaMixin):
    pass


class PushRegistrationBaseSchemaMixin(TrackableSchemaMixin):
    device = marshmallow.auto_field(
        required=True, validate=validate.Length(min=3, max=255)
    )
    platform = EnumField(PushPlatform)
    token = marshmallow.auto_field(required=True)


class PushRegistrationSchema(PushRegistrationIdSchema, PushRegistrationBaseSchemaMixin):
    pass


class PushRegistrationRefSchema(PushRegistrationIdSchema):
    device = marshmallow.auto_field()
    platform = EnumField(PushPlatform)


class PushRegistrationListRequestSchema(PaginationRequestSchema):
    token = fields.Str()


class PushRegistrationListItemSchema(PushRegistrationRefSchema):
    token = marshmallow.auto_field()


class PushRegistrationListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(PushRegistrationListItemSchema),
        metadata={"description": "Push registrations"},
    )


class PushRegistrationPostRequestSchema(
    PushRegistrationModelSchema, PushRegistrationBaseSchemaMixin
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_post_schema()


class PushRegistrationPatchRequestSchema(
    PushRegistrationModelSchema, PushRegistrationBaseSchemaMixin
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_patch_schema()
