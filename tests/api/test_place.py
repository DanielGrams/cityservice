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


def test_recycling_street_list(client, seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()
    place_id = seeder.create_place()
    schreiber_id = seeder.create_recycling_street(
        place_id=place_id, name="Schreiberstraße"
    )
    stadtteil_id = seeder.create_recycling_street(place_id=place_id, name="Stadtteil")
    ortsteil_id = seeder.create_recycling_street(place_id=place_id, name="Ortsteil")

    url = utils.get_url("api_v1_place_recycling_street_list", id=place_id)
    response = utils.get_json(url)
    assert len(response.json["items"]) == 3
    assert response.json["items"][0]["id"] == ortsteil_id
    assert response.json["items"][1]["id"] == stadtteil_id
    assert response.json["items"][2]["id"] == schreiber_id


def test_news_item_list(client, seeder: Seeder, utils: UtilActions):
    place_id = seeder.create_place()
    news_feed_id = seeder.create_news_feed(place_id=place_id)
    seeder.create_news_item(news_feed_id)

    url = utils.get_url("api_v1_place_news_item_list", id=place_id)
    response = utils.get_ok(url)

    assert len(response.json["items"]) == 1

    news_item = response.json["items"][0]
    assert news_item["news_feed"]["publisher"] == "Feuerwehr"
    assert news_item["content"] == "Ein Einsatz war"
    assert news_item["link_url"] == "https://example.com"
    assert news_item["published"] == "2050-01-01T12:00:00+01:00"
    assert (
        news_item["publisher_icon_url"] == "http://localhost/media/taxi-solid-red.png"
    )
