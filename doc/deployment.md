# Deployment

## Automatic Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/DanielGrams/cityservice)

## Cronjobs

flask scrape news
flask scrape weather_warnings
flask scrape recycling
flask user delete-old-anonymous
flask notifications send-recycling-events

## VAPID keys for web push notifications

```sh
env/bin/vapid
env/bin/vapid --applicationServerKey
```

[https://pypi.org/project/py-vapid/]

Set env variables VAPID_CLAIM_EMAIL and VAPID_PRIVATE_KEY.

Print environment variable VAPID_PRIVATE_KEY:

```sh
awk '{printf "%s\\n", $0}' private_key.pem
```

## Certificate for Apple iOS Push notifications

1. Import push services certificate to Mac key chain
2. Select both push services certificate and private key and export (2 items) to cert.p12
3. Call to get env variable APNS_CERT:

```sh
openssl pkcs12 -in cert.p12 -out cert.pem -nodes -clcerts
awk '{printf "%s\\n", $0}' cert.pem
```

## Users

```sh
flask roles add test@test.de admin
```
