from tests.seeder import Seeder
from tests.utils import UtilActions


def test_list(client, seeder: Seeder, utils: UtilActions):
    recycling_street_id = seeder.create_recycling_street()

    url = utils.get_url("api_recycling_street_list")
    response = utils.get_ok(url)

    assert len(response.json) == 1

    news_item = response.json[0]
    assert news_item["id"] == recycling_street_id
    assert news_item["name"] == "Schreiberstraße"
