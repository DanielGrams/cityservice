from tests.seeder import Seeder
from tests.utils import UtilActions


def test_list(client, seeder: Seeder, utils: UtilActions):
    place_id = seeder.create_place()
    recycling_street_id = seeder.create_recycling_street(place_id=place_id)

    url = utils.get_url("api_recycling_street_list")
    response = utils.get_ok(url)

    assert len(response.json) == 1

    news_item = response.json[0]
    assert news_item["id"] == recycling_street_id
    assert news_item["name"] == "Schreiberstraße, Goslar"


def test_read(client, seeder: Seeder, utils: UtilActions):
    place_id = seeder.create_place()
    recycling_street_id = seeder.create_recycling_street(place_id=place_id)

    url = utils.get_url("api_recycling_street", id=recycling_street_id)
    response = utils.get_json(url)
    place = response.json
    assert place["id"] == recycling_street_id
    assert place["name"] == "Schreiberstraße, Goslar"


def test_event_list(client, seeder: Seeder, utils: UtilActions):
    place_id = seeder.create_place()
    recycling_street_id = seeder.create_recycling_street(place_id=place_id)
    event_id = seeder.create_recycling_event(recycling_street_id)

    url = utils.get_url("api_v1_recycling_street_event_list", id=place_id)
    response = utils.get_ok(url)

    assert len(response.json["items"]) == 1

    event_item = response.json["items"][0]
    assert event_item["id"] == event_id
    assert event_item["date"] == "2050-01-01T12:00:00+01:00"
    assert event_item["category"] == "Biotonne"
    assert event_item["category_icon_url"] == "http://localhost/media/1.4.png"
