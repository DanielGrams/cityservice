from tests.seeder import Seeder
from tests.utils import UtilActions


# Load more urls:
# curl -o tests/cli/test_scrape_news/<filename>.rss "<URL>"
def test_scrape(
    client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock
):
    now = utils.mock_now(2022, 1, 25)

    from project.dateutils import create_gmt_date
    from project.models import NewsItem

    _mock_dwd_no_warings(utils, datadir)
    utils.mock_feedparser_http_get(
        "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
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
        assert item.publisher_name == "Stadt Goslar"
        assert item.content == "Verkehrsbehinderungen durch Kundgebung am Montagabend"
        assert item.link_url == item_url
        assert item.published == create_gmt_date(2022, 1, 21, 10, 11, 1)
        assert item.fetched == now


def test_odd_data(
    client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock
):
    utils.mock_now(2022, 1, 25)
    _mock_dwd_no_warings(utils, datadir)
    utils.mock_feedparser_http_get(
        "https://www.goslar.de/presse/pressemitteilungen?format=feed&type=rss",
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
    _mock_dwd_no_warings(utils, datadir)
    utils.mock_feedparser_http_get(
        "http://www.presseportal.de/rss/dienststelle_56518.rss2",
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


def test_dwd(client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock):
    now = utils.mock_now(2022, 1, 25)
    utils.mock_feedparser_http_get()

    # Warnings
    mock_url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
    utils.mock_get_request_with_file(mock_url, datadir, "dwd_warnings.html")

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "news"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.models import NewsItem

        items = NewsItem.query.all()
        assert len(items) == 1

        item = items[0]
        assert item.source_id == "https://www.dwd.de"
        assert item.publisher_name == "Deutscher Wetterdienst"
        assert item.content == "Es liegen Wetterwarnungen vor"
        assert (
            item.link_url
            == "https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html?ort=Goslar"
        )
        assert item.published == now
        assert item.fetched == now

    # No warnings
    _mock_dwd_no_warings(utils, datadir)

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "news"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.models import NewsItem

        items = NewsItem.query.all()
        assert len(items) == 0


def _mock_dwd_no_warings(utils: UtilActions, datadir):
    mock_url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
    utils.mock_get_request_with_file(mock_url, datadir, "dwd_no_warnings.html")
