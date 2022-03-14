from flask_babelex import lazy_gettext


def get_localized_scope(scope: str) -> str:
    loc_key = "Scope_" + scope
    return lazy_gettext(loc_key)


def get_content_from_response(response) -> str:
    try:
        return response.content.decode("UTF-8")
    except Exception:  # pragma: no cover
        return response.content.decode(response.apparent_encoding)
