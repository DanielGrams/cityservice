from functools import wraps

import flask
from flask_apispec.views import MethodResource


def etag_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.add_etag()
        return response.make_conditional(flask.request)

    return wrapper


class BaseResource(MethodResource):
    decorators = [etag_cache]
