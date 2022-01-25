import click
from flask.cli import AppGroup
from flask_migrate import stamp
from sqlalchemy import MetaData

from project import app, db
from project.init_data import create_initial_data

test_cli = AppGroup("test")


@test_cli.command("reset")
@click.option("--seed/--no-seed", default=False)
def reset(seed):
    meta = MetaData(bind=db.engine, reflect=True)
    con = db.engine.connect()
    trans = con.begin()

    for table in meta.sorted_tables:
        con.execute(f'ALTER TABLE "{table.name}" DISABLE TRIGGER ALL;')
        con.execute(table.delete())
        con.execute(f'ALTER TABLE "{table.name}" ENABLE TRIGGER ALL;')

    trans.commit()

    if seed:
        create_initial_data()

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


@test_cli.command("seed")
def seed():
    create_initial_data()
    click.echo("Seed done.")


app.cli.add_command(test_cli)
