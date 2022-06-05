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
docker build -t cityservice:latest .
```

### Run container with existing postgres server

```sh
docker run -p 5000:5000 -e "DATABASE_URL=postgresql://postgres@localhost/cityservice" "cityservice:latest"
```

## Capacitor

### Build for native platforms

```sh
cd frontend
npm run build
npx cap sync
```

### Update with plugin changes

```sh
npx cap sync
```

### Update without plugin changes

```sh
npx cap copy
```

### Run with dev server

- Start Flask server
- Set env variable VUE_APP_BASE_URL to network URL of Flask app.

```sh
cd frontend
npm run serve
```

frontend/capacitor.config.ts

```js
server: {
    "url": "<Network URL of vue app>",
    "cleartext": true,
},
```

```sh
npx cap copy
```
