from flask import request
from flask_babelex import gettext

from project import app, babel


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def print_dynamic_texts():
    gettext("Scope_openid")
    gettext("Scope_profile")
    gettext("Scope_user:read")
    gettext("Scope_user:write")
