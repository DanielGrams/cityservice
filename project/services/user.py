from flask_principal import Permission, RoleNeed
from flask_security import hash_password

from project import user_datastore


def create_user(email, password):
    return user_datastore.create_user(email=email, password=hash_password(password))


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
