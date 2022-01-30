from tests.seeder import Seeder
from tests.utils import UtilActions


def test_read(client, seeder: Seeder, utils: UtilActions):
    seeder.setup_api_access()

    url = utils.get_url("api_user")
    response = utils.get_json(url)

    user = response.json
    assert user["email"] == "test@test.de"
