# Deployment

## Automatic Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/DanielGrams/cityservice)

## Cronjobs

flask scrape news
flask scrape weather_warnings
flask scrape recycling
flask user delete-old-anonymous

## VAPID keys for web push notifications

env/bin/vapid
env/bin/vapid --applicationServerKey

[https://pypi.org/project/py-vapid/]

Set env variables VAPID_CLAIM_EMAIL and VAPID_PRIVATE_KEY.

Print environment variable VAPID_PRIVATE_KEY:

```sh
awk '{printf "%s\\n", $0}' private_key.pem
```
