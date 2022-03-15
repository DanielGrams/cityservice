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
