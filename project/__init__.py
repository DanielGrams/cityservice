import logging
import os

from flask import Flask
from flask_babelex import Babel
from flask_cors import CORS
from flask_gzip import Gzip
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData

from project.custom_session_interface import CustomSessionInterface
from project.utils import make_dir

# Create app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECURITY_URL_PREFIX"] = "/auth"
app.config["SECURITY_CSRF_COOKIE_NAME"] = "XSRF-TOKEN"
app.config["WTF_CSRF_TIME_LIMIT"] = None
app.config["SECURITY_TRACKABLE"] = True
app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
app.config["LANGUAGES"] = ["en", "de"]
app.config["SERVER_NAME"] = os.getenv("SERVER_NAME")
app.config["SECURITY_REGISTERABLE"] = os.environ.get("SECURITY_REGISTERABLE", False)
app.config["VAPID_PRIVATE_KEY"] = os.environ.get("VAPID_PRIVATE_KEY", "").replace(
    r"\n", "\n"
)
app.config["VAPID_CLAIM_EMAIL"] = os.environ.get("VAPID_CLAIM_EMAIL", "")

# Proxy handling
if os.getenv("PREFERRED_URL_SCHEME"):  # pragma: no cover
    app.config["PREFERRED_URL_SCHEME"] = os.getenv("PREFERRED_URL_SCHEME")

from project.reverse_proxied import ReverseProxied

app.wsgi_app = ReverseProxied(app.wsgi_app)

# Generate a nice key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "JL6BFcPC7N23fbKjbSkCM1hTCSn8GsTSb7xT-LF7Z8A"
)
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT", "11853555980110007309421904519904894213"
)

app.config["JWT_PUBLIC_JWKS"] = os.environ.get("JWT_PUBLIC_JWKS", "")
app.config["JWT_PRIVATE_KEY"] = os.environ.get("JWT_PRIVATE_KEY", "").replace(
    r"\n", "\n"
)
app.config["APNS_CERT"] = os.environ.get("APNS_CERT", "").replace(r"\n", "\n")
app.config["APNS_APP_ID"] = os.environ.get("APNS_APP_ID", "")
app.config["APNS_USE_SANDBOX"] = os.getenv("APNS_USE_SANDBOX", False)
app.config["FCM_API_KEY"] = os.environ.get("FCM_API_KEY", "")

# Gunicorn logging
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    if gunicorn_logger.hasHandlers():
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

# Gzip
gzip = Gzip(app)

# Cache pathes
cache_env = os.environ.get("CACHE_PATH", "tmp")
cache_path = (
    cache_env if os.path.isabs(cache_env) else os.path.join(app.root_path, cache_env)
)

# APNS
try:
    make_dir(cache_path)
    apns_cert_path = os.path.join(cache_path, "apns_cert.pem")
    print(app.config["APNS_CERT"], file=open(apns_cert_path, "w"))
except Exception as ex:  # pragma: no cover
    app.logger.exception(ex)

# i18n
app.config["BABEL_DEFAULT_LOCALE"] = "de"
app.config["BABEL_DEFAULT_TIMEZONE"] = "Europe/Berlin"
babel = Babel(app)

# cors
cors = CORS(
    app,
    resources={r"/.well-known/*", r"/api/*", r"/oauth/*", "/swagger/"},
)

# CRSF protection
csrf = CSRFProtect(app)
app.config["WTF_CSRF_CHECK_DEFAULT"] = False

# Create db
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

# API
from project.api import RestApi
from project.forms.security import ExtendedConfirmRegisterForm

# Setup Flask-Security
from project.models import Role, User

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore, register_form=ExtendedConfirmRegisterForm)
app.session_interface = CustomSessionInterface()

# OAuth2
from project.oauth2 import config_oauth

config_oauth(app)

# API Resources
import project.api
import project.cli.notifications

# Command line
import project.cli.scrape
import project.cli.user

if os.getenv("TESTING", False):  # pragma: no cover
    import project.cli.test

from project import i18n, init_data

# Routes
from project.views import frontend, oauth, root

if __name__ == "__main__":  # pragma: no cover
    app.run()
