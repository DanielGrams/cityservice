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


def test_read(client, seeder: Seeder, utils: UtilActions):
    news_feed_id = seeder.create_news_feed()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_news_feed", id=news_feed_id)
    response = utils.get_json(url)
    news_feed = response.json
    assert news_feed["id"] == news_feed_id
    assert news_feed["publisher"] == "Feuerwehr"
    assert news_feed["feed_type"] == "fire_department"
    assert (
        news_feed["url"]
        == "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss"
    )


def test_post(client, app, seeder: Seeder, utils: UtilActions):
    seeder.setup_base(admin=True)

    url = utils.get_url("api_news_feed_list")
    response = utils.post_json(
        url,
        {
            "publisher": "Feuerwehr",
            "url": "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
        },
    )
    utils.assert_response_created(response)
    assert "id" in response.json

    with app.app_context():
        from project.models import NewsFeed, NewsFeedType

        news_feed = NewsFeed.query.get(int(response.json["id"]))
        assert news_feed.publisher == "Feuerwehr"
        assert news_feed.feed_type == NewsFeedType.unknown
        assert (
            news_feed.url
            == "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss"
        )


def test_put(client, seeder: Seeder, utils, app):
    news_feed_id = seeder.create_news_feed()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_news_feed", id=news_feed_id)
    response = utils.put_json(
        url,
        {
            "publisher": "Polizei",
            "url": "http://www.polizei.de",
            "feed_type": "fire_department",
        },
    )
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import NewsFeed, NewsFeedType

        news_feed = NewsFeed.query.get(news_feed_id)
        assert news_feed.publisher == "Polizei"
        assert news_feed.url == "http://www.polizei.de"
        assert news_feed.feed_type == NewsFeedType.fire_department


def test_patch(client, seeder, utils, app):
    news_feed_id = seeder.create_news_feed()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_news_feed", id=news_feed_id)
    response = utils.patch_json(url, {"publisher": "Polizei"})
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import NewsFeed

        news_feed = NewsFeed.query.get(news_feed_id)
        assert news_feed.publisher == "Polizei"
        assert (
            news_feed.url
            == "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss"
        )


def test_delete(client, seeder, utils, app):
    news_feed_id = seeder.create_news_feed()
    seeder.setup_base(admin=True)

    url = utils.get_url("api_news_feed", id=news_feed_id)
    response = utils.delete(url)
    utils.assert_response_no_content(response)

    with app.app_context():
        from project.models import NewsFeed

        news_feed = NewsFeed.query.get(news_feed_id)
        assert news_feed is None
