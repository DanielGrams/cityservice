def drop_db(db):
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")


def test_migrations(app, seeder):
    from flask_migrate import downgrade, upgrade

    from project import db

    with app.app_context():
        drop_db(db)
        upgrade()
        downgrade()
