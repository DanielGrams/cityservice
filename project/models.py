import datetime
import time
from enum import IntEnum

from authlib.integrations.sqla_oauth2 import (
    OAuth2AuthorizationCodeMixin,
    OAuth2ClientMixin,
    OAuth2TokenMixin,
)
from flask import request
from flask_security import RoleMixin, UserMixin, current_user
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Unicode,
    UnicodeText,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, deferred, object_session, relationship

from project import db
from project.dbtypes import IntegerEnum


def _current_user_id_or_none():
    if current_user and current_user.is_authenticated:  # pragma: no cover
        return current_user.id

    return None


class TrackableMixin(object):
    @declared_attr
    def created_at(cls):
        return deferred(
            Column(DateTime, default=datetime.datetime.utcnow), group="trackable"
        )

    @declared_attr
    def updated_at(cls):
        return deferred(
            Column(
                DateTime,
                default=datetime.datetime.utcnow,
                onupdate=datetime.datetime.utcnow,
            ),
            group="trackable",
        )

    @declared_attr
    def created_by_id(cls):
        return deferred(
            Column(
                "created_by_id",
                ForeignKey("user.id"),
                default=_current_user_id_or_none,
            ),
            group="trackable",
        )

    @declared_attr
    def created_by(cls):
        return relationship(
            "User",
            primaryjoin="User.id == %s.created_by_id" % cls.__name__,
            remote_side="User.id",
        )

    @declared_attr
    def updated_by_id(cls):
        return deferred(
            Column(
                "updated_by_id",
                ForeignKey("user.id"),
                default=_current_user_id_or_none,
                onupdate=_current_user_id_or_none,
            ),
            group="trackable",
        )

    @declared_attr
    def updated_by(cls):
        return relationship(
            "User",
            primaryjoin="User.id == %s.updated_by_id" % cls.__name__,
            remote_side="User.id",
        )


# Orte


class Place(db.Model, TrackableMixin):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    recycling_ids = Column(Unicode(255))
    weather_warning_name = Column(Unicode(255))


# OAuth Server: Wir bieten an, dass sich ein Nutzer per OAuth2 auf unserer Seite anmeldet


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = "oauth2_client"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User")

    @OAuth2ClientMixin.grant_types.getter
    def grant_types(self):
        return ["authorization_code", "refresh_token"]

    @OAuth2ClientMixin.response_types.getter
    def response_types(self):
        return ["code"]

    @OAuth2ClientMixin.token_endpoint_auth_method.getter
    def token_endpoint_auth_method(self):
        return ["client_secret_basic", "client_secret_post", "none"]

    def check_redirect_uri(self, redirect_uri):
        if redirect_uri.startswith(request.host_url):  # pragma: no cover
            return True

        return super().check_redirect_uri(redirect_uri)

    def check_token_endpoint_auth_method(self, method):
        return method in self.token_endpoint_auth_method


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = "oauth2_code"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User")


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = "oauth2_token"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User")

    @property
    def client(self):  # pragma: no cover
        return (
            object_session(self)
            .query(OAuth2Client)
            .filter(OAuth2Client.client_id == self.client_id)
            .first()
        )

    def is_refresh_token_active(self):
        if self.revoked:  # pragma: no cover
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()


# News


class NewsFeedType(IntEnum):
    unknown = 1
    city = 2
    district = 3  # Kreis
    police = 4
    fire_department = 5
    culture = 6
    citizen_participation = 7
    civil_protection = 8


class NewsFeed(db.Model, TrackableMixin):
    __tablename__ = "newsfeed"
    id = Column(Integer(), primary_key=True)
    publisher = Column(Unicode(255))
    url = Column(String(255))
    title_filter = Column(Unicode(255))
    title_sub_pattern = Column(Unicode(255))
    title_sub_repl = Column(Unicode(255))
    feed_type = Column(
        IntegerEnum(NewsFeedType),
        nullable=False,
        default=NewsFeedType.unknown.value,
        server_default=str(NewsFeedType.unknown.value),
    )
    news_items = relationship(
        "NewsItem",
        backref=backref("news_feed", lazy=False),
        cascade="all, delete-orphan",
    )
    place_id = Column(db.Integer, db.ForeignKey("place.id"))
    place = relationship("Place", uselist=False)


class NewsItem(db.Model):
    __tablename__ = "newsitems"

    id = db.Column(db.Integer, primary_key=True)
    news_feed_id = db.Column(db.Integer, db.ForeignKey("newsfeed.id"), nullable=False)
    source_id = db.Column(db.String())
    content = db.Column(db.String())
    link_url = db.Column(db.String())
    published = db.Column(db.DateTime(timezone=True))
    fetched = db.Column(db.DateTime(timezone=True))


class WeatherWarning(db.Model):
    __tablename__ = "weatherwarning"

    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String())
    content = db.Column(db.String())
    published = db.Column(db.DateTime(timezone=True))
    start = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    place_id = Column(db.Integer, db.ForeignKey("place.id"))
    place = relationship("Place", uselist=False)


# Recycling


class RecyclingStreet(db.Model):
    __tablename__ = "recyclingstreets"

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String())
    town_id = db.Column(db.String())
    name = db.Column(db.String())
    events = db.relationship("RecyclingEvent", backref="street", lazy=True)
    place_id = Column(db.Integer, db.ForeignKey("place.id"))
    place = relationship("Place", uselist=False)


class RecyclingEvent(db.Model):
    __tablename__ = "recyclingevents"

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String())
    category = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True))
    street_id = db.Column(
        db.Integer, db.ForeignKey("recyclingstreets.id"), nullable=False
    )


# Push


class PushPlatform(IntEnum):
    web = 1
    android = 2
    ios = 3


class PushRegistration(db.Model, TrackableMixin):
    __tablename__ = "pushregistration"
    id = Column(Integer(), primary_key=True)
    token = Column(UnicodeText(), nullable=True)
    device = Column(Unicode(255), nullable=False)
    platform = Column(
        IntegerEnum(PushPlatform),
        nullable=False,
    )
    user_id = Column(Integer(), ForeignKey("user.id"), nullable=False)


# User


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    role_id = Column("role_id", Integer(), ForeignKey("role.id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    title = Column(Unicode(255))
    description = Column(String(255))
    permissions = Column(UnicodeText())


class RecyclingStreetsUsers(db.Model):
    __tablename__ = "recyclingstreets_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    user = relationship("User", backref="user_recyclingstreets")
    recyclingstreet_id = Column(
        "recyclingstreet_id", Integer(), ForeignKey("recyclingstreets.id")
    )
    recyclingstreet = relationship("RecyclingStreet")
    notifications_active = Column(
        Boolean(),
        server_default="0",
        nullable=False,
    )


class PlacesUsers(db.Model):
    __tablename__ = "places_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    place_id = Column("place_id", Integer(), ForeignKey("place.id"))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    anonymous = Column(
        Boolean(),
        server_default="0",
        nullable=False,
    )
    fs_uniquifier = Column(String(255))
    confirmed_at = Column(DateTime())
    roles = relationship(
        "Role", secondary="roles_users", backref=backref("users", lazy="dynamic")
    )
    places = relationship(
        "Place", secondary="places_users", backref=backref("users", lazy="dynamic")
    )
    recyclingstreets = association_proxy("user_recyclingstreets", "recyclingstreet")
    # user_recyclingstreets = relationship("RecyclingStreetsUsers")
    push_registrations = relationship(
        "PushRegistration",
        primaryjoin="User.id == PushRegistration.user_id",
        backref=backref("user", lazy=True),
        cascade="all, delete-orphan",
    )

    def get_user_id(self):
        return self.id

    def get_security_payload(self):
        return {"email": self.email, "roles": [r.name for r in self.roles]}
