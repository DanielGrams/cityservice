from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs

from project import db
from project.api import add_api_resource
from project.api.place.schemas import (
    PlaceIdSchema,
    PlaceListRequestSchema,
    PlaceListResponseSchema,
    PlacePatchRequestSchema,
    PlacePostRequestSchema,
    PlaceSchema,
)
from project.api.resources import (
    BaseResource,
    login_api_user_or_401,
    require_api_access,
)
from project.models import Place
from project.services.place import get_place_query


class PlaceListResource(BaseResource):
    @doc(
        summary="List places",
        tags=["Places"],
        security=[{"oauth2": ["place:read"]}],
    )
    @use_kwargs(PlaceListRequestSchema, location=("query"))
    @marshal_with(PlaceListResponseSchema)
    @require_api_access("place:read")
    def get(self, **kwargs):
        login_api_user_or_401("admin")
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
        security=[{"oauth2": ["place:read"]}],
    )
    @marshal_with(PlaceSchema)
    @require_api_access("place:read")
    def get(self, id):
        login_api_user_or_401("admin")
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


add_api_resource(PlaceListResource, "/places", "api_place_list")
add_api_resource(PlaceResource, "/places/<int:id>", "api_place")
