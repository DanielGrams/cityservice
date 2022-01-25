# Development

## Database

flask db init
flask db migrate
flask db upgrade

## i18n

<https://pythonhosted.org/Flask-BabelEx/>

### Init

```sh
pybabel extract -F babel.cfg -o messages.pot . && pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . && pybabel init -i messages.pot -d project/translations -l de
```

### Add locale

```sh
pybabel init -i messages.pot -d project/translations -l en
```

### Extract new msgid's and merge into \*.po files

```sh
pybabel extract -F babel.cfg -o messages.pot . && pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . && pybabel update -N -i messages.pot -d project/translations
```

#### Compile after translation is done

```sh
pybabel compile -d project/translations
```

## Docker

### Build image

```sh
docker build -t gsevpt:latest .
```

### Run container with existing postgres server

```sh
docker run -p 5000:5000 -e "DATABASE_URL=postgresql://postgres@localhost/gsevpt" "gsevpt:latest"
```
