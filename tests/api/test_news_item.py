from tests.seeder import Seeder
from tests.utils import UtilActions


def test_list(client, seeder: Seeder, utils: UtilActions):
    seeder.create_news_item()

    url = utils.get_url("api_news_item_list")
    response = utils.get_ok(url)

    assert len(response.json) == 1

    news_item = response.json[0]
    assert news_item["publisher_name"] == "Feuerwehr"
    assert news_item["content"] == "Ein Einsatz war"
    assert news_item["link_url"] == "https://example.com"
    assert news_item["published"] == "2050-01-01T12:00:00+01:00"
    assert (
        news_item["publisher_icon_url"] == "http://localhost/media/taxi-solid-red.png"
    )
