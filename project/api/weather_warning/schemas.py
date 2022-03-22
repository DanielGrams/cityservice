from marshmallow import fields

from project.api import marshmallow
from project.api.fields import CustomDateTimeField
from project.api.schemas import (
    IdSchemaMixin,
    PaginationRequestSchema,
    PaginationResponseSchema,
    SQLAlchemyBaseSchema,
)
from project.models import WeatherWarning


class WeatherWarningModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = WeatherWarning
        load_instance = True


class WeatherWarningIdSchema(WeatherWarningModelSchema, IdSchemaMixin):
    pass


class WeatherWarningBaseSchemaMixin(object):
    headline = marshmallow.auto_field()
    content = marshmallow.auto_field()
    published = marshmallow.auto_field()
    published = CustomDateTimeField()
    start = CustomDateTimeField()
    end = CustomDateTimeField()


class WeatherWarningSchema(
    WeatherWarningIdSchema,
    WeatherWarningBaseSchemaMixin,
):
    pass


class WeatherWarningListRequestSchema(PaginationRequestSchema):
    pass


class WeatherWarningListResponseSchema(PaginationResponseSchema):
    items = fields.List(
        fields.Nested(WeatherWarningSchema),
        metadata={"description": "Weather warnings"},
    )


class PlaceWeatherWarningListRequestSchema(WeatherWarningListRequestSchema):
    pass


class PlaceWeatherWarningListResponseSchema(WeatherWarningListResponseSchema):
    pass
