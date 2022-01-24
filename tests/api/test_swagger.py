from swagger_spec_validator import validator20

from tests.utils import UtilActions


def test_swagger(utils: UtilActions):
    response = utils.get_ok("/swagger/")
    validator20.validate_spec(response.json)


def test_swagger_ui(utils: UtilActions):
    utils.get_ok("/swagger-ui/")
