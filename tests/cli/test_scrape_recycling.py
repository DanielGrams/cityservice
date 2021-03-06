from tests.seeder import Seeder
from tests.utils import UtilActions


# Load more urls:
# curl --referer "https://www.kwb-goslar.de" -o tests/cli/test_scrape_recycling/<filename>.rss "<URL>"
def test_scrape(
    client, seeder: Seeder, utils: UtilActions, app, datadir, requests_mock
):
    from project.dateutils import create_berlin_date
    from project.models import RecyclingStreet

    place_id = seeder.create_place()

    # Index
    mock_url = (
        "https://www.kwb-goslar.de/Abfallwirtschaft/Abfuhr/Online-Abfuhrkalender-2022/"
    )
    filename = "index.html"
    utils.mock_get_request_with_file(mock_url, datadir, filename, encoding="latin-1")

    # Town
    town_id = "2523.1"
    mock_url = (
        "https://www.kwb-goslar.de/output/autocomplete.php?out=json&type=abto&mode=&select=2&refid=%s&term="
        % town_id
    )
    filename = "streets-%s.json" % town_id
    utils.mock_get_request_with_file(mock_url, datadir, filename)

    # Street
    street_id = "2523.18"
    mock_url = (
        "https://www.kwb-goslar.de/output/options.php?ModID=48&call=ical&pois=%s&alarm=0"
        % street_id
    )
    filename = "events-%s.ical" % street_id
    utils.mock_get_request_with_file(mock_url, datadir, filename)

    # Invoke
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "recycling"])
    assert "Done." in result.output

    # Create street without place (legacy)
    with app.app_context():
        street = RecyclingStreet.query.first()
        legacy_street_id = seeder.create_recycling_street(
            source_id=street.source_id,
            town_id=street.town_id,
            name=street.name,
        )
        seeder.create_recycling_event(legacy_street_id)

    # Invoke again (to test existing items)
    runner = app.test_cli_runner()
    result = runner.invoke(args=["scrape", "recycling"])
    assert "Done." in result.output

    # Test
    with app.app_context():
        streets = RecyclingStreet.query.all()
        assert len(streets) == 1

        street = streets[0]
        assert street.place_id == place_id
        assert street.source_id == street_id
        assert street.town_id == town_id
        assert street.name == "Ortsteil - Hahndorf, Goslar"

        assert len(street.events) == 81

        event = street.events[0]
        assert event.category == "Restm??lltonne"
        assert event.source_id == "1652da14b6bddda86fc27f4235fca191@www.kwb-goslar.de"
        assert event.date == create_berlin_date(2022, 9, 8, 0)
