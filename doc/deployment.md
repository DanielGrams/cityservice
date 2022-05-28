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

## iOS

### Install fastlane for iOS

```sh
cd frontend/ios/App
bundle install
```

### Deploy to Testflight

- [https://litoarias.medium.com/continuous-delivery-for-ios-using-fastlane-and-github-actions-edf62ee68ecc]
- Setup frontend/ios/App/fastlane/.env

```sh
bundle exec fastlane closed_beta
```

## Android

### Install fastlane for Android

```sh
cd frontend/android
bundle install
```

### Deploy to Playstore

- [https://medium.com/scalereal/automate-publishing-app-to-the-google-play-store-with-github-actions-fastlane-ac9104712486]
- [https://www.runway.team/blog/how-to-build-the-perfect-fastlane-pipeline-for-android]
- Setup frontend/android/fastlane/.env
- Setup frontend/android/keystore.properties
- Put frontend/android/app/google-services.json
- Put frontend/android/play_config.json
- Put frontend/android/app/keystore.jks

```sh
bundle exec fastlane deploy
```
