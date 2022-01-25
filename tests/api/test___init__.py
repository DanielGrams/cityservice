def test_add_oauth2_scheme(app):
    from project.api import add_oauth2_scheme_with_transport

    app.config["SERVER_NAME"] = "127.0.0.1"
    with app.app_context():
        add_oauth2_scheme_with_transport(False)
