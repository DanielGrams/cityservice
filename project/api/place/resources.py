from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from sqlalchemy import func

from project import db
from project.api import add_api_resource
from project.api.news_item.schemas import (
    NewsItemListRequestSchema,
    NewsItemListResponseSchema,
)
from project.api.place.schemas import (
    PlaceIdSchema,
    PlaceListRequestSchema,
    PlaceListResponseSchema,
    PlacePatchRequestSchema,
    PlacePostRequestSchema,
    PlaceSchema,
)
from project.api.recycling_street.schemas import (
    PlaceRecyclingStreetListRequestSchema,
    PlaceRecyclingStreetListResponseSchema,
)
from project.api.resources import (
    BaseResource,
    login_api_user,
    login_api_user_or_401,
    require_api_access,
)
from project.api.weather_warning.schemas import (
    PlaceWeatherWarningListRequestSchema,
    PlaceWeatherWarningListResponseSchema,
)
from project.models import NewsFeed, NewsItem, Place, RecyclingStreet, WeatherWarning
from project.oauth2 import require_oauth
from project.services.place import get_place_query


class PlaceListResource(BaseResource):
    @doc(
        summary="List places",
        tags=["Places"],
    )
    @use_kwargs(PlaceListRequestSchema, location=("query"))
    @marshal_with(PlaceListResponseSchema)
    @require_oauth(optional=True)
    def get(self, **kwargs):
        login_api_user()
        keyword = kwargs["keyword"] if "keyword" in kwargs else None

        pagination = get_place_query(keyword).paginate()
        return pagination

    @doc(
        summary="Add new place",
        tags=["Places"],
        security=[{"oauth2": ["place:write"]}],
    )
    @use_kwargs(PlacePostRequestSchema, location="json", apply=False)
    @marshal_with(PlaceIdSchema)
    @require_api_access("place:write")
    def post(self):
        login_api_user_or_401("admin")

        place = self.create_instance(PlacePostRequestSchema)
        db.session.add(place)
        db.session.commit()

        return place, 201


class PlaceResource(BaseResource):
    @doc(
        summary="Get place",
        tags=["Place"],
    )
    @marshal_with(PlaceSchema)
    @require_oauth(optional=True)
    def get(self, id):
        login_api_user()
        return Place.query.get_or_404(id)

    @doc(
        summary="Update place",
        tags=["Places"],
        security=[{"oauth2": ["place:write"]}],
    )
    @use_kwargs(PlacePostRequestSchema, location="json", apply=False)
    @marshal_with(None, 204)
    @require_api_access("place:write")
    def put(self, id):
        login_api_user_or_401("admin")
        place = Place.query.get_or_404(id)

        place = self.update_instance(PlacePostRequestSchema, instance=place)
        db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Patch place",
        tags=["Places"],
        security=[{"oauth2": ["place:write"]}],
    )
    @use_kwargs(PlacePatchRequestSchema, location="json", apply=False)
    @marshal_with(None, 204)
    @require_api_access("place:write")
    def patch(self, id):
        login_api_user_or_401("admin")
        place = Place.query.get_or_404(id)

        place = self.update_instance(PlacePatchRequestSchema, instance=place)
        db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Delete place",
        tags=["Places"],
        security=[{"oauth2": ["place:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("place:write")
    def delete(self, id):
        login_api_user_or_401("admin")
        place = Place.query.get_or_404(id)

        db.session.delete(place)
        db.session.commit()

        return make_response("", 204)


class PlaceRecyclingStreetListResource(BaseResource):
    @doc(
        summary="List recycling streets of place",
        tags=["Places", "Recycling"],
    )
    @use_kwargs(PlaceRecyclingStreetListRequestSchema, location=("query"))
    @marshal_with(PlaceRecyclingStreetListResponseSchema)
    def get(self, id, **kwargs):
        pagination = (
            RecyclingStreet.query.filter(RecyclingStreet.place_id == id)
            .order_by(
                db.case(((RecyclingStreet.name.ilike("Ortsteil%"), 0),), else_=1),
                db.case(((RecyclingStreet.name.ilike("Stadtteil%"), 0),), else_=1),
                func.lower(RecyclingStreet.name),
            )
            .paginate()
        )
        return pagination


class PlaceNewsItemListResource(BaseResource):
    @doc(
        summary="List news items of place",
        tags=["Places", "News"],
    )
    @use_kwargs(NewsItemListRequestSchema, location=("query"))
    @marshal_with(NewsItemListResponseSchema)
    def get(self, id, **kwargs):
        pagination = (
            NewsItem.query.join(NewsFeed)
            .filter(NewsFeed.place_id == id)
            .order_by(NewsItem.published.desc())
            .paginate()
        )
        return pagination


class PlaceWeatherWarningListResource(BaseResource):
    @doc(
        summary="List weather warnings of place",
        tags=["Places", "Weather"],
    )
    @use_kwargs(PlaceWeatherWarningListRequestSchema, location=("query"))
    @marshal_with(PlaceWeatherWarningListResponseSchema)
    def get(self, id, **kwargs):
        pagination = (
            WeatherWarning.query.filter(WeatherWarning.place_id == id)
            .order_by(WeatherWarning.published.desc())
            .paginate()
        )
        return pagination


add_api_resource(PlaceListResource, "/places", "api_place_list")
add_api_resource(PlaceResource, "/places/<int:id>", "api_place")
add_api_resource(
    PlaceRecyclingStreetListResource,
    "/places/<int:id>/recycling-streets",
    "api_v1_place_recycling_street_list",
)
add_api_resource(
    PlaceNewsItemListResource,
    "/places/<int:id>/news-items",
    "api_v1_place_news_item_list",
)
add_api_resource(
    PlaceWeatherWarningListResource,
    "/places/<int:id>/weather-warnings",
    "api_v1_place_weather_warning_list",
)
