from flask import url_for
from flask.helpers import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_security import current_user

from project import db
from project.api import add_api_resource
from project.api.place.schemas import (
    UserPlaceListRequestSchema,
    UserPlaceListResponseSchema,
)
from project.api.push_registration.schemas import (
    PushRegistrationIdSchema,
    PushRegistrationListRequestSchema,
    PushRegistrationListResponseSchema,
    PushRegistrationPatchRequestSchema,
    PushRegistrationPostRequestSchema,
)
from project.api.recycling_street.schemas import (
    UserRecyclingStreetListRequestSchema,
    UserRecyclingStreetListResponseSchema,
    UserRecyclingStreetPatchRequestSchema,
)
from project.api.resources import (
    BaseResource,
    login_api_user_or_401,
    require_api_access,
)
from project.api.user.schemas import UserSchema
from project.models import (
    Place,
    PushRegistration,
    RecyclingStreet,
    RecyclingStreetsUsers,
)


class UserResource(BaseResource):
    @doc(
        summary="Get user profile",
        tags=["News"],
        security=[{"oauth2": ["profile"]}],
    )
    @marshal_with(UserSchema)
    @require_api_access("profile")
    def get(self, **kwargs):
        login_api_user_or_401()

        return current_user.get_security_payload()


add_api_resource(UserResource, "/user", "api_user")


class UserRecyclingStreetListResource(BaseResource):
    @doc(
        summary="List recycling streets of user",
        tags=["Users", "Recycling"],
        security=[{"oauth2": ["user:read"]}],
    )
    @use_kwargs(UserRecyclingStreetListRequestSchema, location=("query"))
    @marshal_with(UserRecyclingStreetListResponseSchema)
    @require_api_access("user:read")
    def get(self, **kwargs):
        from project.services.user import get_user_recycling_streets_query

        login_api_user_or_401()

        pagination = get_user_recycling_streets_query(current_user.id).paginate()
        return pagination


add_api_resource(
    UserRecyclingStreetListResource,
    "/user/recycling-streets",
    "api_v1_user_recycling_street_list",
)


class UserRecyclingStreetListWriteResource(BaseResource):
    @doc(
        summary="Add recycling streets to user",
        tags=["Users", "Recycling"],
        security=[{"oauth2": ["user:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def put(self, recycling_street_id):
        login_api_user_or_401()
        from project.services.user import add_user_recycling_street

        recycling_street = RecyclingStreet.query.get_or_404(recycling_street_id)

        if add_user_recycling_street(current_user.id, recycling_street.id):
            db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Update recycling street",
        tags=["Users", "Recycling"],
        security=[{"oauth2": ["user:write"]}],
    )
    @use_kwargs(UserRecyclingStreetPatchRequestSchema, location="json", apply=False)
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def patch(self, recycling_street_id):
        login_api_user_or_401()
        user_recycling_street = RecyclingStreetsUsers.query.filter(
            RecyclingStreetsUsers.recyclingstreet_id == recycling_street_id,
            RecyclingStreetsUsers.user_id == current_user.id,
        ).first_or_404()

        user_recycling_street = self.update_instance(
            UserRecyclingStreetPatchRequestSchema, instance=user_recycling_street
        )
        db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Remove recycling streets from user",
        tags=["Users", "Recycling"],
        security=[{"oauth2": ["user:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def delete(self, recycling_street_id):
        from project.services.user import remove_user_recycling_street

        login_api_user_or_401()
        recycling_street = RecyclingStreet.query.get_or_404(recycling_street_id)

        if remove_user_recycling_street(current_user.id, recycling_street.id):
            db.session.commit()

        return make_response("", 204)


add_api_resource(
    UserRecyclingStreetListWriteResource,
    "/user/recycling-streets/<int:recycling_street_id>",
    "api_v1_user_recycling_street_list_write",
)


class UserPlaceListResource(BaseResource):
    @doc(
        summary="List places of user",
        tags=["Users", "Places"],
        security=[{"oauth2": ["user:read"]}],
    )
    @use_kwargs(UserPlaceListRequestSchema, location=("query"))
    @marshal_with(UserPlaceListResponseSchema)
    @require_api_access("user:read")
    def get(self, **kwargs):
        from project.services.user import get_user_places_query

        login_api_user_or_401()

        pagination = get_user_places_query(current_user.id).paginate()
        return pagination


add_api_resource(
    UserPlaceListResource,
    "/user/places",
    "api_v1_user_place_list",
)


class UserPlaceListWriteResource(BaseResource):
    @doc(
        summary="Add places to user",
        tags=["Users", "Places"],
        security=[{"oauth2": ["user:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def put(self, place_id):
        login_api_user_or_401()
        from project.services.user import add_user_place

        place = Place.query.get_or_404(place_id)

        if add_user_place(current_user.id, place.id):
            db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Remove places from user",
        tags=["Users", "Places"],
        security=[{"oauth2": ["user:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def delete(self, place_id):
        from project.services.user import remove_user_place

        login_api_user_or_401()
        place = Place.query.get_or_404(place_id)

        if remove_user_place(current_user.id, place.id):
            db.session.commit()

        return make_response("", 204)


add_api_resource(
    UserPlaceListWriteResource,
    "/user/places/<int:place_id>",
    "api_v1_user_place_list_write",
)


class UserPushRegistrationListResource(BaseResource):
    @doc(
        summary="List push registrations of user",
        tags=["Users", "Push"],
        security=[{"oauth2": ["user:read"]}],
    )
    @use_kwargs(PushRegistrationListRequestSchema, location=("query"))
    @marshal_with(PushRegistrationListResponseSchema)
    @require_api_access("user:read")
    def get(self, **kwargs):
        from project.services.user import get_user_push_registrations_query

        login_api_user_or_401()
        token = kwargs["token"] if "token" in kwargs else None
        pagination = get_user_push_registrations_query(
            current_user.id, token
        ).paginate()
        return pagination

    @doc(
        summary="Add push registration to user",
        tags=["Users", "Push"],
        security=[{"oauth2": ["user:write"]}],
    )
    @use_kwargs(PushRegistrationPostRequestSchema, location="json", apply=False)
    @marshal_with(PushRegistrationIdSchema, 201)
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def post(self):
        login_api_user_or_401()
        from project.services.user import upsert_user_push_registration

        push_registration = self.create_instance(PushRegistrationPostRequestSchema)
        created = upsert_user_push_registration(current_user.id, push_registration)
        db.session.commit()

        if created:
            return push_registration, 201

        return make_response("", 204)


add_api_resource(
    UserPushRegistrationListResource,
    "/user/push-registrations",
    "api_v1_user_push_registration_list",
)


class UserPushRegistrationListWriteResource(BaseResource):
    @doc(
        summary="Remove push registration from user",
        tags=["Users", "Push"],
        security=[{"oauth2": ["user:write"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def delete(self, id):
        login_api_user_or_401()
        push_registration = PushRegistration.query.get_or_404(id)

        db.session.delete(push_registration)
        db.session.commit()

        return make_response("", 204)

    @doc(
        summary="Update push registration",
        tags=["Users", "Push"],
        security=[{"oauth2": ["user:write"]}],
    )
    @use_kwargs(PushRegistrationPatchRequestSchema, location="json", apply=False)
    @marshal_with(None, 204)
    @require_api_access("user:write")
    def patch(self, id):
        login_api_user_or_401()
        push_registration = PushRegistration.query.get_or_404(id)

        push_registration = self.update_instance(
            PushRegistrationPatchRequestSchema, instance=push_registration
        )
        db.session.commit()

        return make_response("", 204)


add_api_resource(
    UserPushRegistrationListWriteResource,
    "/user/push-registrations/<int:id>",
    "api_v1_user_push_registration_list_write",
)


class UserPushRegistrationSendResource(BaseResource):
    @doc(
        summary="Send test notification to registration",
        tags=["Users", "Push"],
        security=[{"oauth2": ["user:read"]}],
    )
    @marshal_with(None, 204)
    @require_api_access("user:read")
    def post(self, id):
        login_api_user_or_401()
        from project.services.notification import send_notification

        push_registration = PushRegistration.query.get_or_404(id)
        base_url = url_for("frontend.index", _external=True)
        send_notification(push_registration, "Test message", base_url)

        return make_response("", 204)


add_api_resource(
    UserPushRegistrationSendResource,
    "/user/push-registrations/<int:id>/send",
    "api_v1_user_push_registration_send",
)
