from project.api import marshmallow
from project.api.schemas import SQLAlchemyBaseSchema
from project.models import RecyclingStreet


class RecyclingStreetSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingStreet
        load_instance = True

    id = marshmallow.auto_field()
    name = marshmallow.auto_field()
