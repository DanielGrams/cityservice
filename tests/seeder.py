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
        from flask_security.confirmable import confirm_user

        from project.services.user import (
            add_admin_roles_to_user,
            create_user,
            find_user_by_email,
        )

        with self._app.app_context():
            user = find_user_by_email(email)

            if user is None:
                user = create_user(email, password)
                confirm_user(user)

            if admin:
                add_admin_roles_to_user(email)

            self._db.session.commit()
            user_id = user.id

        return user_id

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

    def setup_api_access(self, admin=True):
        user_id = self.setup_base(admin=admin, log_in=False)
        return self.authorize_api_access(user_id)

    def authorize_api_access(self, user_id):
        oauth2_client_id = self.insert_default_oauth2_client(user_id)

        with self._app.app_context():
            from project.models import OAuth2Client

            oauth2_client = OAuth2Client.query.get(oauth2_client_id)
            client_id = oauth2_client.client_id
            client_secret = oauth2_client.client_secret
            scope = oauth2_client.scope

        self._utils.login(follow_redirects=False)
        self._utils.authorize(client_id, client_secret, scope)
        self._utils.logout()
        return user_id

    def create_news_item(self, **kwargs) -> int:
        with self._app.app_context():
            news_item_id = self._model_seeder.create_news_item(**kwargs)

        return news_item_id

    def create_news_feed(self, **kwargs) -> int:
        with self._app.app_context():
            news_feed_id = self._model_seeder.create_news_feed(**kwargs)

        return news_feed_id

    def create_recycling_street(self, **kwargs) -> int:
        from project.models import RecyclingStreet

        with self._app.app_context():
            recycling_street = RecyclingStreet()
            recycling_street.town_id = (
                kwargs["town_id"] if "town_id" in kwargs else "38640"
            )
            recycling_street.name = (
                kwargs["name"] if "name" in kwargs else "Schreiberstraße"
            )

            self._db.session.add(recycling_street)
            self._db.session.commit()
            recycling_street_id = recycling_street.id

        return recycling_street_id

    def create_recycling_event(self, street_id: int, **kwargs) -> int:
        from project.dateutils import create_berlin_date
        from project.models import RecyclingEvent

        with self._app.app_context():
            recycling_event = RecyclingEvent()
            recycling_event.street_id = street_id
            recycling_event.category = (
                kwargs["category"] if "category" in kwargs else "Biotonne"
            )
            recycling_event.date = (
                kwargs["date"]
                if "date" in kwargs
                else create_berlin_date(2050, 1, 1, 12)
            )

            self._db.session.add(recycling_event)
            self._db.session.commit()
            recycling_event_id = recycling_event.id

        return recycling_event_id
