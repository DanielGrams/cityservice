from marshmallow import fields

from project.api import marshmallow
from project.api.fields import CustomDateTimeField


class NewsItemSchema(marshmallow.Schema):
    publisher_name = fields.Str()
    content = fields.Str()
    link_url = fields.Str()
    published = CustomDateTimeField()
    publisher_icon_url = fields.Str()
