from tests.seeder import Seeder
from tests.utils import UtilActions


def test_list(client, seeder: Seeder, utils: UtilActions):
    seeder.setup_base(admin=True)
    seeder.create_place()

    url = utils.get_url("api_place_list")
    response = utils.get_json(url)

    items = response.json["items"]
    assert len(items) == 1

    place = items[0]
    assert place["name"] == "Goslar"

    url = utils.get_url("api_place_list", keyword="Goslar")
    response = utils.get_json(url)


def test_read(client, seeder: Seeder, utils: UtilActions):
    place_id = seeder.create_place()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_place", id=place_id)
    response = utils.get_json(url)
    place = response.json
    assert place["id"] == place_id
    assert place["name"] == "Goslar"


def test_post(client, app, seeder: Seeder, utils: UtilActions):
    seeder.setup_base(admin=True)

    url = utils.get_url("api_place_list")
    response = utils.post_json(
        url,
        {
            "name": "Goslar",
        },
    )
    utils.assert_response_created(response)
    assert "id" in response.json

    with app.app_context():
        from project.models import Place

        place = Place.query.get(int(response.json["id"]))
        assert place.name == "Goslar"


def test_put(client, seeder: Seeder, utils, app):
    place_id = seeder.create_place()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_place", id=place_id)
    response = utils.put_json(
        url,
        {
            "name": "Seesen",
        },
    )
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import Place

        place = Place.query.get(place_id)
        assert place.name == "Seesen"


def test_patch(client, seeder, utils, app):
    place_id = seeder.create_place()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_place", id=place_id)
    response = utils.patch_json(url, {"name": "Seesen"})
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import Place

        place = Place.query.get(place_id)
        assert place.name == "Seesen"
        assert place.weather_warning_name == "Stadt Goslar"


def test_delete(client, seeder, utils, app):
    place_id = seeder.create_place()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_place", id=place_id)
    response = utils.delete(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import Place

        place = Place.query.get(place_id)
        assert place is None
