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
from project.models import NewsFeed, NewsFeedType


class NewsFeedModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = NewsFeed
        load_instance = True


class NewsFeedIdSchema(NewsFeedModelSchema, IdSchemaMixin):
    pass


class NewsFeedWriteIdSchema(NewsFeedModelSchema, WriteIdSchemaMixin):
    pass


class NewsFeedBaseSchemaMixin(TrackableSchemaMixin):
    publisher = marshmallow.auto_field(
        required=True, validate=validate.Length(min=3, max=255)
    )
    url = marshmallow.auto_field(
        required=True, validate=[validate.URL(), validate.Length(max=255)]
    )
    url = marshmallow.auto_field(required=True, validate=[validate.Length(max=255)])
    title_filter = marshmallow.auto_field(validate=[validate.Length(max=255)])
    title_sub_pattern = marshmallow.auto_field(validate=[validate.Length(max=255)])
    title_sub_repl = marshmallow.auto_field(validate=[validate.Length(max=255)])
    feed_type = EnumField(
        NewsFeedType,
        missing=NewsFeedType.unknown,
    )


class NewsFeedSchema(NewsFeedIdSchema, NewsFeedBaseSchemaMixin):
    pass


class NewsFeedRefSchema(NewsFeedIdSchema):
    publisher = marshmallow.auto_field()
    feed_type = EnumField(NewsFeedType)


class NewsFeedListRequestSchema(PaginationRequestSchema):
    pass


class NewsFeedListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(NewsFeedRefSchema), metadata={"description": "News feeds"}
    )


class NewsFeedPostRequestSchema(NewsFeedModelSchema, NewsFeedBaseSchemaMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_post_schema()


class NewsFeedPatchRequestSchema(NewsFeedModelSchema, NewsFeedBaseSchemaMixin):
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        self.make_patch_schema()
