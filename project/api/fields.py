from marshmallow import fields

from project.dateutils import berlin_tz


class CustomDateTimeField(fields.DateTime):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            value = value.astimezone(berlin_tz)

        return super()._serialize(value, attr, obj, **kwargs)
