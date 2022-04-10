from tests.seeder import Seeder
from tests.utils import UtilActions


def test_read(client, seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()

    url = utils.get_url("api_user")
    response = utils.get_json(url)

    user = response.json
    assert user["email"] == "test@test.de"


def test_recycling_street_list(client, seeder: Seeder, utils: UtilActions):
    user_id = seeder.setup_api_access()
    recycling_street_id = seeder.create_recycling_street()
    seeder.add_user_recycling_street(user_id, recycling_street_id)

    url = utils.get_url("api_v1_user_recycling_street_list")
    response = utils.get_json(url)
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["id"] == recycling_street_id

    seeder.remove_user_recycling_street(user_id, recycling_street_id)

    url = utils.get_url("api_v1_user_recycling_street_list")
    response = utils.get_json(url)
    assert len(response.json["items"]) == 0


def test_recycling_street_list_put(client, seeder: Seeder, utils: UtilActions, app):
    user_id = seeder.setup_api_access()
    recycling_street_id = seeder.create_recycling_street()

    url = utils.get_url(
        "api_v1_user_recycling_street_list_write",
        recycling_street_id=recycling_street_id,
    )
    response = utils.put_json(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.services.user import get_user_recycling_street

        user_recycling_street = get_user_recycling_street(user_id, recycling_street_id)
        assert user_recycling_street is not None


def test_recycling_street_list_delete(client, seeder: Seeder, utils: UtilActions, app):
    user_id = seeder.setup_api_access()
    recycling_street_id = seeder.create_recycling_street()
    seeder.add_user_recycling_street(user_id, recycling_street_id)

    url = utils.get_url(
        "api_v1_user_recycling_street_list_write",
        recycling_street_id=recycling_street_id,
    )
    response = utils.delete(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.services.user import get_user_recycling_street

        user_recycling_street = get_user_recycling_street(user_id, recycling_street_id)
        assert user_recycling_street is None


def test_place_list(client, seeder: Seeder, utils: UtilActions):
    user_id = seeder.setup_api_access()
    place_id = seeder.create_place()
    seeder.add_user_place(user_id, place_id)

    url = utils.get_url("api_v1_user_place_list")
    response = utils.get_json(url)
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["id"] == place_id

    seeder.remove_user_place(user_id, place_id)

    url = utils.get_url("api_v1_user_place_list")
    response = utils.get_json(url)
    assert len(response.json["items"]) == 0


def test_place_list_put(client, seeder: Seeder, utils: UtilActions, app):
    user_id = seeder.setup_api_access()
    place_id = seeder.create_place()

    url = utils.get_url(
        "api_v1_user_place_list_write",
        place_id=place_id,
    )
    response = utils.put_json(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.services.user import get_user_place

        user_place = get_user_place(user_id, place_id)
        assert user_place is not None


def test_place_list_delete(client, seeder: Seeder, utils: UtilActions, app):
    user_id = seeder.setup_api_access()
    place_id = seeder.create_place()
    seeder.add_user_place(user_id, place_id)

    url = utils.get_url(
        "api_v1_user_place_list_write",
        place_id=place_id,
    )
    response = utils.delete(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.services.user import get_user_place

        user_place = get_user_place(user_id, place_id)
        assert user_place is None


def test_push_registration_list(client, seeder: Seeder, utils: UtilActions):
    user_id = seeder.setup_api_access()
    push_registration_id = seeder.upsert_push_registration(user_id)

    url = utils.get_url("api_v1_user_push_registration_list")
    response = utils.get_json(url)
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["id"] == push_registration_id

    token = "testtoken"
    push_registration_id = seeder.upsert_push_registration(user_id, token=token)

    url = utils.get_url("api_v1_user_push_registration_list", token=token)
    response = utils.get_json(url)
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["id"] == push_registration_id


def test_push_registration_list_post(client, seeder: Seeder, utils: UtilActions, app):
    import json

    user_id = seeder.setup_api_access()

    url = utils.get_url(
        "api_v1_user_push_registration_list",
    )
    data = {
        "device": "Chrome Browser",
        "platform": "web",
        "token": json.dumps(
            {
                "endpoint": "https://fcm.googleapis.com/fcm/send/55555",
                "expirationTime": None,
                "keys": {
                    "p256dh": "qo35jtlwkert",
                    "auth": "lkjashkfhgksjdhfg",
                },
            }
        ),
    }
    response = utils.post_json(
        url,
        data,
    )
    utils.assert_response_created(response)
    assert "id" in response.json

    with app.app_context():
        from project.models import PushPlatform, PushRegistration

        registration = PushRegistration.query.get(int(response.json["id"]))
        assert registration.device == "Chrome Browser"
        assert registration.platform == PushPlatform.web
        assert registration.user_id == user_id

        token = json.loads(registration.token)
        assert token["endpoint"] == "https://fcm.googleapis.com/fcm/send/55555"
        assert token["expirationTime"] is None
        assert token["keys"]["p256dh"] == "qo35jtlwkert"
        assert token["keys"]["auth"] == "lkjashkfhgksjdhfg"

    response = utils.post_json(
        url,
        data,
    )
    utils.assert_response_no_content(response)


def test_push_registration_list_delete(client, seeder: Seeder, utils: UtilActions, app):
    user_id = seeder.setup_api_access()
    push_registration_id = seeder.upsert_push_registration(user_id)

    url = utils.get_url(
        "api_v1_user_push_registration_list_write",
        id=push_registration_id,
    )
    response = utils.delete(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import PushRegistration

        registration = PushRegistration.query.get(push_registration_id)
        assert registration is None


def test_push_registration_send(
    client, seeder: Seeder, utils: UtilActions, app, mocker
):
    user_id = seeder.setup_api_access()
    push_registration_id = seeder.upsert_push_registration(user_id)

    mock = mocker.patch("project.services.notification.send_notification")

    url = utils.get_url(
        "api_v1_user_push_registration_send",
        id=push_registration_id,
    )
    response = utils.post_json(url, None)
    utils.assert_response_no_content(response)

    mock.assert_called_once()
