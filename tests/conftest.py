import os
import warnings

import pytest
from sqlalchemy.exc import SAWarning

from .seeder import Seeder
from .utils import UtilActions


def pytest_generate_tests(metafunc):
    warnings.filterwarnings("error", category=SAWarning)

    os.environ["DATABASE_URL"] = os.environ.get(
        "TEST_DATABASE_URL", "postgresql://postgres@localhost/cityservice_tests"
    )


@pytest.fixture
def app():
    from project import app

    app.config["SERVER_NAME"] = None
    app.config["TESTING"] = True
    app.testing = True

    return app


@pytest.fixture
def db(app):
    from flask_migrate import stamp

    from project import db

    with app.app_context():
        db.drop_all()
        db.create_all()
        stamp()

    return db


@pytest.fixture
def client(app, db):
    return app.test_client()


@pytest.fixture
def utils(client, app, mocker, requests_mock):
    return UtilActions(client, app, mocker, requests_mock)


@pytest.fixture
def seeder(app, db, utils):
    return Seeder(app, db, utils)
