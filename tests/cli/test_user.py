from tests.utils import UtilActions


def test_delete_old_anonymous(app, db, utils: UtilActions):
    now = utils.mock_now(2022, 3, 9)

    with app.app_context():
        from datetime import timedelta

        from project.services.user import create_user, create_user_anonymous

        normal_user = create_user("test@test.de", "geheim")
        new_anonymous_user = create_user_anonymous()
        old_anonymous_user = create_user_anonymous()
        old_anonymous_user.last_login_at = now - timedelta(days=367)
        db.session.commit()

        normal_user_id = normal_user.id
        new_anonymous_user_id = new_anonymous_user.id
        old_anonymous_user_id = old_anonymous_user.id

    runner = app.test_cli_runner()
    result = runner.invoke(args=["user", "delete-old-anonymous"])
    assert "Old anonymous users were deleted." in result.output

    with app.app_context():
        from project.models import User

        assert User.query.get(normal_user_id) is not None
        assert User.query.get(new_anonymous_user_id) is not None
        assert User.query.get(old_anonymous_user_id) is None
