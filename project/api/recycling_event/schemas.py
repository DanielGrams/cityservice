from project.api.schemas import SQLAlchemyBaseSchema
from project.models import RecyclingEvent


class RecyclingEventSchema(SQLAlchemyBaseSchema):
    class Meta:
        model = RecyclingEvent
        fields = ("date", "category", "category_icon_url")


recycling_event_schema = RecyclingEventSchema()
recycling_events_schema = RecyclingEventSchema(many=True)
