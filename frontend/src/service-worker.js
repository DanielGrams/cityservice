/* eslint-disable no-undef */
importScripts("localforage.min.js");

workbox.core.setCacheNameDetails({ prefix: "frontend" });
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

var store = localforage.createInstance({
  name: "sw",
});

function handlePushUpdate() {
  return store.getItem("pushInfo").then((pushInfo) => {
    if (!pushInfo) {
      return;
    }

    return self.registration.pushManager
      .getSubscription()
      .then((newSubscription) => {
        const oldSubscription = pushInfo.subscription;
        if (JSON.stringify(oldSubscription) == JSON.stringify(newSubscription)) {
          return;
        }

        pushInfo.subscription = JSON.parse(JSON.stringify(newSubscription));
        return store.setItem("pushInfo", pushInfo).then(() => {
          return fetch(
            `/api/user/push-registrations/${pushInfo.pushRegistrationId}`,
            {
              method: "patch",
              credentials: "same-origin",
              headers: {
                "Content-type": "application/json",
              },
              body: JSON.stringify({
                token: JSON.stringify(newSubscription),
              }),
            }
          );
        });
      });
  });
}

function savePushRegistration(pushRegistrationId, subscription) {
  const pushInfo = {
    pushRegistrationId: pushRegistrationId,
    subscription: subscription,
  };
  return store.setItem("pushInfo", pushInfo);
}

function deletePushRegistration() {
  return store.removeItem("pushInfo");
}

function handlePushLoaded(pushRegistrationId, subscription) {
  return store.getItem("pushInfo").then((pushInfo) => {
    if (!pushInfo) {
      return savePushRegistration(pushRegistrationId, subscription);
    }

    return handlePushUpdate();
  });
}

self.addEventListener("message", (event) => {
  if (event.data) {
    if (event.data.type === "SKIP_WAITING") {
      self.skipWaiting();
    } else if (event.data.action === "PUSH_LOADED") {
      event.waitUntil(
        handlePushLoaded(event.data.pushRegistrationId, event.data.subscription)
      );
    } else if (event.data.action === "PUSH_REGISTERED") {
      event.waitUntil(
        savePushRegistration(
          event.data.pushRegistrationId,
          event.data.subscription
        )
      );
    } else if (event.data.action === "PUSH_UNREGISTERED") {
      event.waitUntil(deletePushRegistration());
    }
  }
});

self.addEventListener("push", (event) => {
  if (!(self.Notification && self.Notification.permission === "granted")) {
    return;
  }

  if (event.data == null) {
    return;
  }

  var text = event.data.text();
  var payload;
  try {
    payload = JSON.parse(text);
  } catch (e) {
    payload = {
      options: {
        body: text,
      },
    };
  }

  if (payload.title == null) {
    payload.title = "City service";
  }

  event.waitUntil(
    self.registration.showNotification(payload.title, payload.options)
  );
});

self.addEventListener("notificationclick", (event) => {
  var notification = event.notification;
  notification.close();

  if (notification.data != null && notification.data.url) {
    // eslint-disable-next-line no-undef
    clients.openWindow(notification.data.url);
  }
});

self.addEventListener("pushsubscriptionchange", (event) => {
  event.waitUntil(handlePushUpdate());
});
