import os

from project import app, db
from project.api import add_oauth2_scheme_with_transport
from project.services.user import upsert_user_role


@app.before_first_request
def add_oauth2_scheme():
    # At some sites the https scheme is not set yet
    insecure = os.getenv("AUTHLIB_INSECURE_TRANSPORT", "False").lower() in ["true", "1"]
    add_oauth2_scheme_with_transport(insecure)


@app.before_first_request
def create_initial_data():
    admin_permissions = [
        "admin_unit:update",
        "admin_unit.members:invite",
        "admin_unit.members:read",
        "admin_unit.members:update",
        "admin_unit.members:delete",
    ]
    early_adopter_permissions = [
        "oauth2_client:create",
        "oauth2_client:read",
        "oauth2_client:update",
        "oauth2_client:delete",
        "oauth2_token:create",
        "oauth2_token:read",
        "oauth2_token:update",
        "oauth2_token:delete",
    ]

    upsert_user_role("admin", "Administrator", admin_permissions)
    upsert_user_role("early_adopter", "Early Adopter", early_adopter_permissions)

    db.session.commit()
