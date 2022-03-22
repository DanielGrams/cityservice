from tests.seeder import Seeder
from tests.utils import UtilActions


def test_list(client, seeder: Seeder, utils: UtilActions):
    recycling_street_id = seeder.create_recycling_street()
    seeder.create_recycling_event(recycling_street_id)

    url = utils.get_url(
        "api_recycling_street_event_list", street_id=recycling_street_id
    )
    response = utils.get_ok(url)

    assert len(response.json) == 1

    event_item = response.json[0]
    assert event_item["date"] == "2050-01-01T12:00:00+01:00"
    assert event_item["category"] == "Biotonne"
    assert event_item["category_icon_url"] == "http://localhost/media/1.4.png"

    # All
    url = utils.get_url(
        "api_recycling_street_event_list", street_id=recycling_street_id, all=1
    )
    response = utils.get_ok(url)
    assert len(response.json) == 1


def test_list_street_before_2022(client, seeder: Seeder, utils: UtilActions):
    street_id = seeder.create_recycling_street()
    seeder.create_recycling_event(street_id)
    old_street_id = seeder.create_recycling_street(town_id="4711")

    url = utils.get_url("api_recycling_street_event_list", street_id=old_street_id)
    response = utils.get_ok(url)

    assert len(response.json) == 1

    event_item = response.json[0]
    assert event_item["date"] == "2050-01-01T12:00:00+01:00"
    assert event_item["category"] == "Biotonne"
    assert event_item["category_icon_url"] == "http://localhost/media/1.4.png"
