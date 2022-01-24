from flask_apispec import doc, marshal_with
from sqlalchemy.sql.expression import func

from project.api import add_api_resource
from project.api.recycling_street.schemas import (
    RecyclingStreetSchema,
    recycling_streets_schema,
)
from project.api.resources import BaseResource
from project.models import RecyclingStreet


class RecyclingStreetList(BaseResource):
    @doc(summary="List recycling street", tags=["Recycling"])
    @marshal_with(RecyclingStreetSchema(many=True))
    def get(self):
        items = RecyclingStreet.query.filter(
            func.length(RecyclingStreet.town_id) > 4
        ).all()  # > 4 bedeutet TownId ab 2022

        sorted_items = sorted(
            items,
            key=lambda item: (
                not item.name.startswith("Ortsteil")
                and not item.name.startswith("Stadtteil"),
                item.name,
            ),
        )
        return recycling_streets_schema.dump(sorted_items)


add_api_resource(RecyclingStreetList, "/recycling/streets", "api_recycling_street_list")