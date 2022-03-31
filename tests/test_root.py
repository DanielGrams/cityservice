from tests.seeder import Seeder
from tests.utils import UtilActions


def test_root(client, seeder: Seeder, utils: UtilActions):
    utils.get_endpoint_ok("frontend.index")
    utils.get_endpoint_ok("serve_file_in_dir", path="city-solid.png")
