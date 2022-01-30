import pytest

from tests.seeder import Seeder
from tests.utils import UtilActions


@pytest.mark.parametrize("auth", ["none", "normal", "admin"])
def test_list(client, seeder: Seeder, utils: UtilActions, auth):
    seeder.create_news_feed()

    if auth == "normal":
        seeder.setup_base(admin=False)
    elif auth == "admin":
        seeder.setup_base(admin=True)

    url = utils.get_url("api_news_feed_list")
    response = utils.get_json(url)

    if auth != "admin":
        utils.assert_response_unauthorized(response)
        return

    items = response.json["items"]
    assert len(items) == 1

    news_feed = items[0]
    assert news_feed["publisher"] == "Feuerwehr"
