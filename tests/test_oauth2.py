from tests.seeder import Seeder
from tests.utils import UtilActions


def test_authorization_code(seeder: Seeder):
    seeder.setup_api_access()


def test_refresh_token(seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()
    utils.refresh_token()
