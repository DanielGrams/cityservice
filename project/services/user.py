import datetime
import secrets

from flask_security import hash_password
from sqlalchemy import func
from sqlalchemy.sql import and_

from project import user_datastore
from project.dateutils import get_now


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
