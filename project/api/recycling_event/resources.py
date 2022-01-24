import flask
from flask_apispec import doc, marshal_with
from sqlalchemy import and_

from project.api import add_api_resource
from project.api.recycling_event.schemas import (
    RecyclingEventSchema,
    recycling_events_schema,
)
from project.api.resources import BaseResource
from project.dateutils import get_today
from project.models import RecyclingEvent, RecyclingStreet


class RecyclingEventList(BaseResource):
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

        for item in items:  # pragma: no cover
            if item.category == "Baum- und Strauchschnitt":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="1.5.png", _external=True
                )
            elif item.category == "Biotonne":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="1.4.png", _external=True
                )
            elif item.category == "Blaue Tonne":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="1.3.png", _external=True
                )
            elif item.category == "Gelber Sack":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="1.2.png", _external=True
                )
            elif item.category == "Restmülltonne":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="1.1.png", _external=True
                )
            elif item.category == "Weihnachtsbäume":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="1.6.png", _external=True
                )
            elif item.category == "Wertstofftonne danach":
                item.category_icon_url = flask.url_for(
                    "serve_file_in_dir", path="2523.1.png", _external=True
                )

        return recycling_events_schema.dump(items)


add_api_resource(
    RecyclingEventList,
    "/recycling/street/<street_id>/events",
    "api_recycling_street_event_list",
)
