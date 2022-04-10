from typing import Tuple

from tests.model_seeder import ModelSeeder
from tests.utils import UtilActions


class Seeder(object):
    def __init__(self, app, db, utils: UtilActions):
        self._app = app
        self._db = db
        self._utils = utils
        self._model_seeder = ModelSeeder(db)

    def setup_base(
        self,
        admin=False,
        log_in=True,
        email="test@test.de",
    ):
        user_id = self.create_user(email=email, admin=admin)
        if log_in:
            self._utils.login()
        return user_id

    def create_user(
        self, email="test@test.de", password="MeinPasswortIstDasBeste", admin=False
    ):
        with self._app.app_context():
            return self._model_seeder.create_user(email, password, admin)

    def insert_default_oauth2_client(self, user_id):
        from project.api import scope_list
        from project.models import OAuth2Client
        from project.services.oauth2_client import complete_oauth2_client

        with self._app.app_context():
            client = OAuth2Client()
            client.user_id = user_id
            complete_oauth2_client(client)

            metadata = dict()
            metadata["client_name"] = "Mein Client"
            metadata["scope"] = " ".join(scope_list)
            metadata["grant_types"] = ["authorization_code", "refresh_token"]
            metadata["response_types"] = ["code"]
            metadata["token_endpoint_auth_method"] = "client_secret_post"
            metadata["redirect_uris"] = [self._utils.get_url("swagger_oauth2_redirect")]
            client.set_client_metadata(metadata)

            self._db.session.add(client)
            self._db.session.commit()
            client_id = client.id

        return client_id

    def get_oauth2_client(self, oauth2_client_id: int) -> Tuple:
        with self._app.app_context():
            from project.models import OAuth2Client

            oauth2_client = OAuth2Client.query.get(oauth2_client_id)
            client_id = oauth2_client.client_id
            client_secret = oauth2_client.client_secret
            scope = oauth2_client.scope

        return (client_id, client_secret, scope)

    def setup_api_access(self, admin=True) -> int:
        user_id = self.setup_base(admin=admin, log_in=False)
        return self.authorize_api_access(user_id)

    def authorize_api_access(self, user_id) -> int:
        oauth2_client_id = self.insert_default_oauth2_client(user_id)
        client_id, client_secret, scope = self.get_oauth2_client(oauth2_client_id)

        self._utils.login(follow_redirects=False)
        self._utils.authorize(client_id, client_secret, scope)
        self._utils.logout()
        return user_id

    def authorize_api_access_anonymous(self):
        user_id = self.create_user()
        oauth2_client_id = self.insert_default_oauth2_client(user_id)
        client_id, client_secret, scope = self.get_oauth2_client(oauth2_client_id)

        self._utils.authorize_anonymous(client_id, client_secret, scope)

    def create_news_item(self, news_feed_id: int, **kwargs) -> int:
        with self._app.app_context():
            news_item_id = self._model_seeder.create_news_item(news_feed_id, **kwargs)

        return news_item_id

    def create_news_feed(self, **kwargs) -> int:
        with self._app.app_context():
            news_feed_id = self._model_seeder.create_news_feed(**kwargs)

        return news_feed_id

    def create_place(self, **kwargs) -> int:
        with self._app.app_context():
            place_id = self._model_seeder.create_place(**kwargs)

        return place_id

    def create_weather_warning(self, **kwargs) -> int:
        with self._app.app_context():
            weather_warning_id = self._model_seeder.create_weather_warning(**kwargs)

        return weather_warning_id

    def create_recycling_street(self, **kwargs) -> int:
        with self._app.app_context():
            recycling_street_id = self._model_seeder.create_recycling_street(**kwargs)

        return recycling_street_id

    def create_recycling_event(self, street_id: int, **kwargs) -> int:
        with self._app.app_context():
            recycling_event_id = self._model_seeder.create_recycling_event(
                street_id, **kwargs
            )

        return recycling_event_id

    def add_user_recycling_street(self, user_id, recyclingstreet_id):
        with self._app.app_context():
            self._model_seeder.add_user_recycling_street(user_id, recyclingstreet_id)

    def remove_user_recycling_street(self, user_id, recyclingstreet_id):
        with self._app.app_context():
            self._model_seeder.remove_user_recycling_street(user_id, recyclingstreet_id)

    def add_user_place(self, user_id, place_id):
        with self._app.app_context():
            self._model_seeder.add_user_place(user_id, place_id)

    def remove_user_place(self, user_id, place_id):
        with self._app.app_context():
            self._model_seeder.remove_user_place(user_id, place_id)

    def create_common_scenario(self):
        with self._app.app_context():
            self._model_seeder.create_common_scenario()

    def upsert_push_registration(self, user_id: int, **kwargs) -> int:
        with self._app.app_context():
            registration_id = self._model_seeder.upsert_push_registration(
                user_id, **kwargs
            )

        return registration_id
