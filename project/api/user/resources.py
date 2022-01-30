from flask_apispec import doc, marshal_with
from flask_security import current_user

from project.api import add_api_resource
from project.api.resources import (
    BaseResource,
    login_api_user_or_401,
    require_api_access,
)
from project.api.user.schemas import UserSchema


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
