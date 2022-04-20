from tests.seeder import Seeder
from tests.utils import UtilActions


def test_send_recycling_events(app, db, seeder: Seeder, utils: UtilActions):
    from project.dateutils import create_berlin_date

    utils.mock_now(2022, 4, 20, 18)
    tomorrow = create_berlin_date(2022, 4, 21)
    mock = utils.mock_webpush()

    user_id = seeder.create_user()
    recycling_street_id = seeder.create_recycling_street()
    seeder.add_user_recycling_street(user_id, recycling_street_id)
    seeder.create_recycling_event(recycling_street_id, date=tomorrow)
    seeder.upsert_push_registration(user_id)

    runner = app.test_cli_runner()
    result = runner.invoke(args=["notifications", "send-recycling-events"])
    assert "1 notifications were sent, 0 errors." in result.output

    mock.assert_called_once()
