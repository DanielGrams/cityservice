import datetime
import secrets

from flask_security import hash_password
from sqlalchemy import func
from sqlalchemy.sql import and_

from project import user_datastore
from project.dateutils import get_now
from project.models import (
    Place,
    PlacesUsers,
    PushRegistration,
    RecyclingStreet,
    RecyclingStreetsUsers,
)


def create_user(email, password):
    return user_datastore.create_user(email=email, password=hash_password(password))


def create_user_anonymous():
    from project.models import User

    max_id_row = user_datastore.db.session.query(func.max(User.id)).first()
    max_id = max_id_row[0] if max_id_row[0] else 0
    email = f"anonymous{max_id + 1}@cityservice.de"
    password = secrets.token_urlsafe(32)

    user = create_user(email, password)
    user.anonymous = True
    user_datastore.commit()
    return user


def delete_old_anonymous_users():
    from project.models import User

    now = get_now()
    min_date = now - datetime.timedelta(days=366)

    User.query.filter(and_(User.anonymous, User.last_login_at <= min_date)).delete(
        synchronize_session=False
    )
    user_datastore.commit()


def find_user_by_email(email):
    return user_datastore.find_user(email=email, case_insensitive=True)


def add_roles_to_user(email, roles):
    user = find_user_by_email(email)

    if user is None:  # pragma: no cover
        raise ValueError("User with given email does not exist.")

    for role in roles:
        user_datastore.add_role_to_user(user, role)


def add_admin_roles_to_user(email):
    add_roles_to_user(email, ["admin", "early_adopter"])


def upsert_user_role(role_name, role_title, permissions):
    role = user_datastore.find_or_create_role(role_name)
    role.title = role_title
    role.remove_permissions(role.get_permissions())
    role.add_permissions(permissions)
    return role


def get_user_recycling_streets_query(user_id: int):
    return RecyclingStreet.query.join(
        RecyclingStreetsUsers,
        RecyclingStreetsUsers.recyclingstreet_id == RecyclingStreet.id,
    ).filter(RecyclingStreetsUsers.user_id == user_id)


def get_user_recycling_street(user_id: int, recyclingstreet_id: int) -> RecyclingStreet:
    return RecyclingStreetsUsers.query.filter(
        RecyclingStreetsUsers.recyclingstreet_id == recyclingstreet_id,
        RecyclingStreetsUsers.user_id == user_id,
    ).first()


def has_user_recycling_street(user_id: int, recyclingstreet_id: int) -> bool:
    if get_user_recycling_street(user_id, recyclingstreet_id):  # pragma: no cover
        return True

    return False


def add_user_recycling_street(user_id: int, recyclingstreet_id: int) -> bool:
    from project import db

    if has_user_recycling_street(user_id, recyclingstreet_id):  # pragma: no cover
        return False

    user_recycling_street = RecyclingStreetsUsers(
        user_id=user_id, recyclingstreet_id=recyclingstreet_id
    )
    db.session.add(user_recycling_street)
    return True


def remove_user_recycling_street(user_id: int, recyclingstreet_id: int):
    from project import db

    user_recycling_street = get_user_recycling_street(user_id, recyclingstreet_id)

    if not user_recycling_street:  # pragma: no cover
        return False

    db.session.delete(user_recycling_street)
    return True


def get_user_places_query(user_id: int):
    return Place.query.join(
        PlacesUsers,
        PlacesUsers.place_id == Place.id,
    ).filter(PlacesUsers.user_id == user_id)


def get_user_place(user_id: int, place_id: int) -> Place:
    return PlacesUsers.query.filter(
        PlacesUsers.place_id == place_id,
        PlacesUsers.user_id == user_id,
    ).first()


def has_user_place(user_id: int, place_id: int) -> bool:
    if get_user_place(user_id, place_id):  # pragma: no cover
        return True

    return False


def add_user_place(user_id: int, place_id: int) -> bool:
    from project import db

    if has_user_place(user_id, place_id):  # pragma: no cover
        return False

    user_place = PlacesUsers(user_id=user_id, place_id=place_id)
    db.session.add(user_place)
    return True


def remove_user_place(user_id: int, place_id: int):
    from project import db

    user_place = get_user_place(user_id, place_id)

    if not user_place:  # pragma: no cover
        return False

    db.session.delete(user_place)
    return True


def get_user_push_registrations_query(user_id: int, token=None):
    query = PushRegistration.query.filter(PushRegistration.user_id == user_id)

    if token:
        query = query.filter(PushRegistration.token == token)

    return query


def upsert_user_push_registration(user_id: int, registration: PushRegistration) -> bool:
    from project import db

    existing = (
        get_user_push_registrations_query(user_id)
        .filter(PushRegistration.token == registration.token)
        .first()
    )

    if existing:
        existing.device = registration.device
    else:
        registration.user_id = user_id
        db.session.add(registration)

    return not existing
