def test_event_category(client, app, db, seeder):
    with app.app_context():
        from project.models import NewsItem

        item = NewsItem()
        assert item is not None
