from marshmallow import fields

from project.api import marshmallow
from project.api.schemas import SQLAlchemyBaseSchema
from project.models import User


class UserModelSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = User
        load_instance = True


class UserSchema(UserModelSchema):
    email = marshmallow.auto_field()
    roles = fields.List(fields.Str())
