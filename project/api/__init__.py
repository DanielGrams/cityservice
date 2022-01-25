from apispec import APISpec
from apispec.exceptions import DuplicateComponentNameError
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import url_for
from flask_apispec.extension import FlaskApiSpec
from flask_marshmallow import Marshmallow
from flask_restful import Api

from project import app
from project.utils import get_localized_scope


class RestApi(Api):
    pass


scope_list = ["openid", "profile", "user:read", "user:write"]
scopes = {k: get_localized_scope(k) for v, k in enumerate(scope_list)}


rest_api = RestApi(app, "/api", catch_all_404s=True)
marshmallow = Marshmallow(app)
marshmallow_plugin = MarshmallowPlugin()
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Cityservice API",
            version="0.1.0",
            plugins=[marshmallow_plugin],
            openapi_version="2.0",
            info=dict(
                description="This API provides endpoints to interact with the Cityservice data."
            ),
        ),
    }
)

api_docs = FlaskApiSpec(app)


def enum_to_properties(self, field, **kwargs):  # pragma: no cover
    """
    Add an OpenAPI extension for marshmallow_enum.EnumField instances
    """
    import marshmallow_enum

    if isinstance(field, marshmallow_enum.EnumField):
        return {"type": "string", "enum": [m.name for m in field.enum]}
    return {}


def add_api_resource(resource, url, endpoint):
    rest_api.add_resource(resource, url, endpoint=endpoint)
    api_docs.register(resource, endpoint=endpoint)


def add_oauth2_scheme_with_transport(insecure: bool):
    if insecure:
        authorizationUrl = url_for("authorize", _external=True)
        tokenUrl = url_for("issue_token", _external=True)
    else:
        authorizationUrl = url_for("authorize", _external=True, _scheme="https")
        tokenUrl = url_for("issue_token", _external=True, _scheme="https")

    oauth2_scheme = {
        "type": "oauth2",
        "authorizationUrl": authorizationUrl,
        "tokenUrl": tokenUrl,
        "flow": "accessCode",
        "scopes": {k: k for _, k in enumerate(scope_list)},
    }

    try:
        api_docs.spec.components.security_scheme("oauth2", oauth2_scheme)
    except DuplicateComponentNameError:  # pragma: no cover
        pass


marshmallow_plugin.converter.add_attribute_function(enum_to_properties)

import project.api.news_item.resources
import project.api.recycling_event.resources
import project.api.recycling_street.resources
