from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_marshmallow import Marshmallow
from flask_restful import Api

from project import app


class RestApi(Api):
    pass


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


def add_api_resource(resource, url, endpoint):
    rest_api.add_resource(resource, url, endpoint=endpoint)
    api_docs.register(resource, endpoint=endpoint)


import project.api.news_item.resources
import project.api.recycling_event.resources
import project.api.recycling_street.resources
