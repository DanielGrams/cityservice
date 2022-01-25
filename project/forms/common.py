from flask import url_for
from flask_babelex import lazy_gettext
from markupsafe import Markup


def get_accept_tos_markup():
    tos_open = '<a href="%s">' % url_for("impressum")
    tos_close = "</a>"

    privacy_open = '<a href="%s">' % url_for("datenschutz")
    privacy_close = "</a>"

    return Markup(
        lazy_gettext(
            "I read and accept %(tos_open)sTerms of Service%(tos_close)s and %(privacy_open)sPrivacy%(privacy_close)s.",
            tos_open=tos_open,
            tos_close=tos_close,
            privacy_open=privacy_open,
            privacy_close=privacy_close,
        )
    )
