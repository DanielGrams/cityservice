from tests.seeder import Seeder
from tests.utils import UtilActions


def test_register(client, app, utils: UtilActions):
    utils.register("test@test.de", "MeinPasswortIstDasBeste")

    with app.app_context():
        from project.services.user import find_user_by_email

        user = find_user_by_email("test@test.de")
        assert user is not None


def test_login(client, app, db, utils: UtilActions, seeder: Seeder):
    seeder.create_user("test@test.de", "MeinPasswortIstDasBeste")
    user_id = utils.login("test@test.de", "MeinPasswortIstDasBeste")
    assert user_id is not None
