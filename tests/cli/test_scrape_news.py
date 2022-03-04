from tests.seeder import Seeder
from tests.utils import UtilActions


# Load more urls:
# curl -o tests/cli/test_scrape_news/<filename>.rss "<URL>"
def test_scrape(
    client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock
):
    now = utils.mock_now(2022, 1, 25)
    feed_url = "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss"
    news_feed_id = seeder.create_news_feed(url=feed_url)

    from project.dateutils import create_gmt_date
    from project.models import NewsItem

    utils.mock_feedparser_http_get(
        feed_url,
        datadir,
        "stadt_goslar.rss",
    )

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "news"])
    assert "Done." in result.output

    # Invoke again (to test existing items)
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "news"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        items = NewsItem.query.all()
        assert len(items) == 4

        item = items[0]
        item_url = "https://www.goslar.de/presse/pressemitteilungen/verkehr-strassen/289724-verkehrsbehinderungen-durch-kundgebung-am-montagabend"
        assert item.source_id == item_url
        assert item.news_feed_id == news_feed_id
        assert item.content == "Verkehrsbehinderungen durch Kundgebung am Montagabend"
        assert item.link_url == item_url
        assert item.published == create_gmt_date(2022, 1, 21, 10, 11, 1)
        assert item.fetched == now


def test_odd_data(
    client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock
):
    utils.mock_now(2022, 1, 25)
    feed_url = "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss"
    seeder.create_news_feed(url=feed_url)
    utils.mock_feedparser_http_get(
        feed_url,
        datadir,
        "odd_data.rss",
    )

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "news"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.models import NewsItem

        items = NewsItem.query.filter(NewsItem.content == "Ohne pubDate").all()
        assert len(items) == 0

        items = NewsItem.query.filter(NewsItem.content == "Zu alt").all()
        assert len(items) == 0

        items = NewsItem.query.filter(NewsItem.content == "Ohne ID").all()
        assert len(items) == 1


def test_pol(client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock):
    utils.mock_now(2022, 1, 25)
    feed_url = "http://www.presseportal.de/rss/dienststelle_56518.rss2"
    seeder.create_news_feed(
        url=feed_url,
        title_filter=".*Goslar|Vienenburg.*",
        title_sub_pattern="POL-GS: ",
        title_sub_repl="",
    )
    utils.mock_feedparser_http_get(
        feed_url,
        datadir,
        "pol_goslar.rss",
    )

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "news"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.models import NewsItem

        items = NewsItem.query.filter(
            NewsItem.content
            == "Pressemitteilung der Polizeiinspektion Goslar vom 24.01.2022"
        ).all()
        assert len(items) == 1

        items = NewsItem.query.filter(
            NewsItem.content
            == "Pressebericht des PK Bad Harzburg vom 22.01.2022 bis 23.01.2022"
        ).all()
        assert len(items) == 0
