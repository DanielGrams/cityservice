from project.api.schemas import SQLAlchemyBaseSchema
from project.models import RecyclingStreet


class RecyclingStreetSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingStreet
        fields = ("id", "name")


recycling_street_schema = RecyclingStreetSchema()
recycling_streets_schema = RecyclingStreetSchema(many=True)
