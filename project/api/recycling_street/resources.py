from flask_apispec import doc, marshal_with, use_kwargs
from sqlalchemy.sql.expression import func

from project.api import add_api_resource
from project.api.recycling_event.schemas import (
    RecyclingStreetEventListRequestSchema,
    RecyclingStreetEventListResponseSchema,
)
from project.api.recycling_street.schemas import RecyclingStreetSchema
from project.api.resources import BaseResource, login_api_user
from project.dateutils import get_today
from project.models import RecyclingEvent, RecyclingStreet
from project.oauth2 import require_oauth
from project.services.place import get_place_query


class LegacyRecyclingStreetListResource(BaseResource):
    @doc(summary="List recycling streets", tags=["Recycling"])
    @marshal_with(RecyclingStreetSchema(many=True))
    def get(self):
        # Legacy: Goslar only
        place = get_place_query("Goslar").first()
        place_id = place.id if place else None

        items = (
            RecyclingStreet.query.filter(RecyclingStreet.place_id == place_id)
            .filter(func.length(RecyclingStreet.town_id) > 4)
            .all()
        )  # > 4 bedeutet TownId ab 2022

        sorted_items = sorted(
            items,
            key=lambda item: (
                not item.name.startswith("Ortsteil")
                and not item.name.startswith("Stadtteil"),
                item.name,
            ),
        )
        return sorted_items


class RecyclingStreetResource(BaseResource):
    @doc(
        summary="Get recycling street",
        tags=["Recycling"],
    )
    @marshal_with(RecyclingStreetSchema)
    @require_oauth(optional=True)
    def get(self, id):
        login_api_user()
        return RecyclingStreet.query.get_or_404(id)


class RecyclingStreetEventListResource(BaseResource):
    @doc(
        summary="List events of recycling street",
        tags=["Recycling"],
    )
    @use_kwargs(RecyclingStreetEventListRequestSchema, location=("query"))
    @marshal_with(RecyclingStreetEventListResponseSchema)
    def get(self, id, **kwargs):
        query = RecyclingEvent.query.filter(RecyclingEvent.street_id == id)

        if "all" not in kwargs:
            today = get_today()
            query = query.filter(RecyclingEvent.date >= today)

        return query.order_by(RecyclingEvent.date).paginate()


add_api_resource(
    LegacyRecyclingStreetListResource, "/recycling/streets", "api_recycling_street_list"
)
add_api_resource(
    RecyclingStreetResource, "/recycling-streets/<int:id>", "api_recycling_street"
)
add_api_resource(
    RecyclingStreetEventListResource,
    "/recycling-streets/<int:id>/events",
    "api_v1_recycling_street_event_list",
)
