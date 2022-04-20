import click
from flask.cli import AppGroup

from project import app

notifications_cli = AppGroup("notifications")


@notifications_cli.command("send-recycling-events")
def send_recycling_events():
    from project.services.notification import send_recycling_events

    success_count, error_count = send_recycling_events()
    click.echo(f"{success_count} notifications were sent, {error_count} errors.")


app.cli.add_command(notifications_cli)
