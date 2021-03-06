from functools import wraps

from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from authlib.oauth2.rfc6749 import MissingAuthorizationError
from flask import abort, request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from flask_login import login_user
from flask_security import current_user

from project import db
from project.api.schemas import ErrorResponseSchema, UnprocessableEntityResponseSchema
from project.oauth2 import require_oauth


def etag_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.add_etag()
        return response.make_conditional(request)

    return wrapper


def require_api_access(scope=None, operator="AND", optional=False):
    def inner_decorator(func):
        def wrapped(*args, **kwargs):  # see authlib ResourceProtector#__call__
            try:
                try:
                    require_oauth.acquire_token(scope, operator)
                except MissingAuthorizationError as error:
                    if optional:  # pragma: no cover
                        return func(*args, **kwargs)
                    require_oauth.raise_error_response(error)
                except OAuth2Error as error:  # pragma: no cover
                    require_oauth.raise_error_response(error)
            except Exception as e:
                if not current_user or not current_user.is_authenticated:
                    raise e
            return func(*args, **kwargs)

        return wrapped

    return inner_decorator


def login_api_user() -> bool:
    return (
        current_token
        and login_user(current_token.user)
        or current_user
        and current_user.is_authenticated
    )


def login_api_user_or_401(role: str = None) -> bool:
    if not login_api_user():  # pragma: no cover
        abort(401)

    if role and not current_user.has_role(role):
        abort(401)


@marshal_with(ErrorResponseSchema, 400, "Bad Request")
@marshal_with(UnprocessableEntityResponseSchema, 422, "Unprocessable Entity")
class BaseResource(MethodResource):
    decorators = [etag_cache]

    def create_instance(self, schema_cls, **kwargs):  # pragma: no cover
        instance = schema_cls().load(request.json, session=db.session)

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        validate = getattr(instance, "validate", None)
        if callable(validate):
            validate()

        return instance

    def update_instance(self, schema_cls, instance):  # pragma: no cover
        with db.session.no_autoflush:
            instance = schema_cls().load(
                request.json, session=db.session, instance=instance
            )

            validate = getattr(instance, "validate", None)
            if callable(validate):
                validate()

        return instance
