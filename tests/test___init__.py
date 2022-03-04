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
        news_feed_id = seeder.create_news_feed()
        seeder.create_news_item(news_feed_id)
        street_id = seeder.create_recycling_street()
        seeder.create_recycling_event(street_id)
        downgrade()


def test_migration_news_feeds(app, seeder: Seeder):
    import sqlalchemy
    from flask_migrate import upgrade

    from project import db
    from project.models import NewsItem

    with app.app_context():
        drop_db(db)
        upgrade(revision="f94690e0b957")

        sql = """
DO $$
DECLARE
    news_item_id newsitems.id%TYPE;
BEGIN
    INSERT INTO newsitems (content) VALUES ('content') RETURNING id INTO news_item_id;
END $$;
                """
        db.engine.execute(sqlalchemy.text(sql).execution_options(autocommit=True))

        upgrade()

        news_items = NewsItem.query.all()
        assert len(news_items) == 0
