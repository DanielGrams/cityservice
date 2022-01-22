python manage.py db init
python manage.py db migrate
python manage.py db upgrade

= Heroku Buildpacks =
heroku/nodejs
heroku/python

= Heroku settings =
NPM_CONFIG_PRODUCTION=false
USE_NPM_INSTALL=true

heroku run flask db upgrade --app goslar-service
