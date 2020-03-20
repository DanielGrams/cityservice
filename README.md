python manage.py db init
python manage.py db migrate
python manage.py db upgrade

heroku run python manage.py db upgrade --app goslar-service