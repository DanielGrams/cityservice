from tests.seeder import Seeder
from tests.utils import UtilActions


def test_send_recycling_events(app, db, seeder: Seeder, utils: UtilActions):
    app.config["SERVER_NAME"] = "127.0.0.1"
    with app.app_context():
        from project.dateutils import create_berlin_date
        from project.services.notification import send_recycling_events

        utils.mock_now(2022, 4, 20, 18)
        tomorrow = create_berlin_date(2022, 4, 21)

        user_id = seeder.create_user()
        recycling_street_id = seeder.create_recycling_street()
        seeder.add_user_recycling_street(user_id, recycling_street_id)
        seeder.set_user_recycling_street_notifications_active(
            user_id, recycling_street_id, True
        )
        seeder.create_recycling_event(recycling_street_id, date=tomorrow)
        push_registration_id = seeder.upsert_push_registration(user_id)

        mock = utils.mock_webpush()
        success_count, error_count = send_recycling_events()
        assert success_count == 1
        assert error_count == 0

        mock.assert_called_once()
        args, _ = mock.call_args
        registration, message, url = args
        assert registration.id == push_registration_id
        assert message == "Schreiberstraße, Goslar: Biotonne"
        assert url == f"http://127.0.0.1/recycling-streets/{recycling_street_id}"
