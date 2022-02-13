from tests.seeder import Seeder


def drop_db(db):
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")


def test_migrations(app, seeder: Seeder):
    from flask_migrate import downgrade, upgrade

    from project import db
    from project.init_data import create_initial_data

    with app.app_context():
        drop_db(db)
        upgrade()
        create_initial_data()
        seeder.create_news_feed()
        seeder.create_news_item()
        street_id = seeder.create_recycling_street()
        seeder.create_recycling_event(street_id)
        downgrade()
