from tests.seeder import Seeder
from tests.utils import UtilActions


def test_authorize_unauthorizedRedirects(seeder: Seeder, utils: UtilActions):
    url = utils.get_url("authorize")
    response = utils.get(url)

    assert response.status_code == 302
    assert "login" in response.headers["Location"]


def test_authorize_validateThrowsError(seeder: Seeder, utils: UtilActions):
    seeder.setup_base()
    url = utils.get_url("authorize")
    response = utils.get(url)

    utils.assert_response_bad_request(response)


def test_revoke_token(seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()
    utils.revoke_token()


def test_introspect(seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()
    utils.introspect(utils.get_access_token(), "access_token")
    utils.introspect(utils.get_refresh_token(), "refresh_token")
    utils.introspect(utils.get_access_token(), "")
    utils.introspect(utils.get_refresh_token(), "")


def test_swagger_redirect(utils):
    url = utils.get_url("swagger_oauth2_redirect")
    response = utils.get(url)
    assert response.status_code == 302


def test_oauth_userinfo(seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()
    utils.get_oauth_userinfo()


def test_jwks(utils):
    utils.get_endpoint_ok("jwks")


def test_openid_configuration(utils):
    utils.get_endpoint_ok("openid_configuration")


def test_authorize_anonymous(app, seeder: Seeder, utils: UtilActions):
    seeder.authorize_api_access_anonymous()

    with app.app_context():
        from project.services.user import find_user_by_email

        user = find_user_by_email("anonymous2@cityservice.de")
        assert user is not None
        assert user.anonymous
