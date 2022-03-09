import click
from flask.cli import AppGroup

from project import app
from project.services.user import delete_old_anonymous_users

user_cli = AppGroup("user")


@user_cli.command("delete-old-anonymous")
def delete_old_anonymous():
    delete_old_anonymous_users()
    click.echo("Old anonymous users were deleted.")


app.cli.add_command(user_cli)
