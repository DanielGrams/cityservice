from tests.seeder import Seeder
from tests.utils import UtilActions


# Load more urls:
# curl -o tests/cli/test_scrape_weather_warnings/<filename>.html "<URL>"
def test_scrape(
    client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock
):
    utils.mock_now(2022, 3, 4)
    utils.mock_feedparser_http_get()
    place_id = seeder.create_place()

    # Warnings
    mock_url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
    utils.mock_get_request_with_file(mock_url, datadir, "dwd_warnings.html")

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "weather_warnings"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.dateutils import create_berlin_date
        from project.models import WeatherWarning

        items = WeatherWarning.query.all()
        assert len(items) == 1

        item = items[0]
        assert item.headline == "Amtliche WARNUNG vor FROST"
        assert item.content == "Es tritt mäßiger Frost zwischen -3 °C und -6 °C auf."
        assert item.start == create_berlin_date(2022, 3, 3, 19)
        assert item.end == create_berlin_date(2022, 3, 4, 10)
        assert item.published == create_berlin_date(2022, 3, 4, 7, 33)
        assert item.place_id == place_id

    # No warnings
    utils.mock_get_request_with_file(mock_url, datadir, "dwd_no_warnings.html")

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "weather_warnings"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.models import WeatherWarning

        items = WeatherWarning.query.all()
        assert len(items) == 0

    # March warnings
    utils.mock_get_request_with_file(mock_url, datadir, "dwd_march.html")

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "weather_warnings"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        from project.models import WeatherWarning

        items = WeatherWarning.query.all()
        assert len(items) == 1


def test_april_data(client, seeder: Seeder, utils: UtilActions, app, datadir):
    from project.cli.scrape_weather_warnings import scrape

    utils.mock_now(2022, 3, 4)
    place_id = seeder.create_place(
        name="Goslar",
        weather_warning_name="Stadt Goslar",
    )

    # Warnings
    mock_url = "https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nib.html"
    utils.mock_get_request_with_file(mock_url, datadir, "dwd_april.html")

    scrape()

    # Test
    with app.app_context():
        from project.dateutils import create_berlin_date
        from project.models import WeatherWarning

        items = WeatherWarning.query.filter(WeatherWarning.place_id == place_id).all()
        assert len(items) == 3

        item = items[0]
        assert item.headline == "Amtliche WARNUNG vor LEICHTEM SCHNEEFALL"
        assert (
            item.content
            == "Es tritt im Warnzeitraum leichter Schneefall mit Mengen zwischen 5 cm und 10 cm auf. In Staulagen werden Mengen bis 15 cm erreicht. Verbreitet wird es glatt."
        )
        assert item.start == create_berlin_date(2022, 3, 31, 20)
        assert item.end == create_berlin_date(2022, 4, 1, 10)
        assert item.published == create_berlin_date(2022, 4, 1, 7, 17)


def test_parse_date_time(client, seeder: Seeder, utils: UtilActions, app):
    from project.cli.scrape_weather_warnings import _parse_date_time
    from project.dateutils import create_berlin_date

    now = utils.mock_now(2022, 12, 31)
    result = _parse_date_time(now, "So, 01. Jan, 10:00 Uhr")
    assert result == create_berlin_date(2023, 1, 1, 10, 0)

    now = utils.mock_now(2022, 3, 31)
    result = _parse_date_time(now, "Do., 31. März, 07:49 Uhr")
    assert result == create_berlin_date(2022, 3, 31, 7, 49)
