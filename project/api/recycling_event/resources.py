import flask
from flask_apispec import doc, marshal_with
from sqlalchemy import and_

from project.api import add_api_resource
from project.api.recycling_event.schemas import RecyclingEventSchema
from project.api.resources import BaseResource
from project.dateutils import get_today
from project.models import RecyclingEvent, RecyclingStreet


class RecyclingEventListResource(BaseResource):
    @doc(summary="List recycling events for street", tags=["Recycling"])
    @marshal_with(RecyclingEventSchema(many=True))
    def get(self, street_id):
        street = RecyclingStreet.query.filter_by(id=street_id).first_or_404(
            description="Die Straße ist nicht vorhanden."
        )

        street_ids = list()
        if len(street.town_id) > 4:  # > 4 bedeutet TownId ab 2022
            street_ids.append(street.id)
        else:  # wenn street mit alter town_id, dann alle streets laden, die denselben namen haben
            similar_streets = RecyclingStreet.query.filter(
                RecyclingStreet.name == street.name
            ).all()
            for similar_street in similar_streets:
                street_ids.append(similar_street.id)

        if "all" in flask.request.args:
            items = (
                RecyclingEvent.query.filter(RecyclingEvent.street_id.in_(street_ids))
                .order_by(RecyclingEvent.date)
                .all()
            )
        else:
            today = get_today()
            items = (
                RecyclingEvent.query.filter(
                    and_(
                        RecyclingEvent.street_id.in_(street_ids),
                        RecyclingEvent.date >= today,
                    )
                )
                .order_by(RecyclingEvent.date)
                .all()
            )

        return items


add_api_resource(
    RecyclingEventListResource,
    "/recycling/street/<street_id>/events",
    "api_recycling_street_event_list",
)
