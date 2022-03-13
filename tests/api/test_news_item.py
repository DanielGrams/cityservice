import pytest

from tests.seeder import Seeder
from tests.utils import UtilActions


@pytest.mark.parametrize("with_place", [False, True])
def test_list(client, seeder: Seeder, utils: UtilActions, with_place):
    place_id = seeder.create_place() if with_place else None
    news_feed_id = seeder.create_news_feed(place_id=place_id)
    seeder.create_news_item(news_feed_id)
    seeder.create_weather_warning(place_id=place_id)

    url = utils.get_url("api_news_item_list")
    response = utils.get_ok(url)

    assert len(response.json) == 2

    news_item = response.json[0]
    assert news_item["publisher_name"] == "Deutscher Wetterdienst"
    assert news_item["content"] == "Amtliche WARNUNG vor FROST"
    assert (
        news_item["link_url"]
        == "https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html?ort=Goslar"
    )
    assert news_item["published"] == "2050-01-01T13:00:00+01:00"
    assert news_item["publisher_icon_url"] == "http://localhost/media/warning-solid.png"

    news_item = response.json[1]
    assert news_item["publisher_name"] == "Feuerwehr"
    assert news_item["content"] == "Ein Einsatz war"
    assert news_item["link_url"] == "https://example.com"
    assert news_item["published"] == "2050-01-01T12:00:00+01:00"
    assert (
        news_item["publisher_icon_url"] == "http://localhost/media/taxi-solid-red.png"
    )


def test_two_weather_warnings(client, seeder: Seeder, utils: UtilActions):
    seeder.create_weather_warning()
    seeder.create_weather_warning(headline="Amtliche WARNUNG vor STURM")

    url = utils.get_url("api_news_item_list")
    response = utils.get_ok(url)

    assert len(response.json) == 1
    news_item = response.json[0]
    assert news_item["content"] == "Amtliche WARNUNG vor FROST und eine weitere Warnung"


def test_more_weather_warnings(client, seeder: Seeder, utils: UtilActions):
    seeder.create_weather_warning()
    seeder.create_weather_warning(headline="Amtliche WARNUNG vor STURM")
    seeder.create_weather_warning(headline="Amtliche WARNUNG vor NEBEL")

    url = utils.get_url("api_news_item_list")
    response = utils.get_ok(url)

    assert len(response.json) == 1
    news_item = response.json[0]
    assert news_item["content"] == "Amtliche WARNUNG vor FROST und 2 weitere Warnungen"
