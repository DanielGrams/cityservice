import click
from flask.cli import AppGroup
from flask_migrate import stamp
from sqlalchemy import MetaData

from project import app, db

test_cli = AppGroup("test")


@test_cli.command("reset")
def reset():
    meta = MetaData(bind=db.engine, reflect=True)
    con = db.engine.connect()
    trans = con.begin()

    for table in meta.sorted_tables:
        con.execute(f'ALTER TABLE "{table.name}" DISABLE TRIGGER ALL;')
        con.execute(table.delete())
        con.execute(f'ALTER TABLE "{table.name}" ENABLE TRIGGER ALL;')

    trans.commit()

    click.echo("Reset done.")


@test_cli.command("drop-all")
def drop_all():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    click.echo("Drop all done.")


@test_cli.command("create-all")
def create_all():
    stamp()
    db.create_all()
    click.echo("Create all done.")


app.cli.add_command(test_cli)
