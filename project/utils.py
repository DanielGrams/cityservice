from flask_babelex import lazy_gettext


def get_localized_scope(scope: str) -> str:
    loc_key = "Scope_" + scope
    return lazy_gettext(loc_key)
