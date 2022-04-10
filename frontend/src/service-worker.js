// eslint-disable-next-line no-undef
workbox.core.setCacheNameDetails({prefix: "frontend"});

self.__precacheManifest = [].concat(self.__precacheManifest || []);
// eslint-disable-next-line no-undef
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('push', (event) => {
  if (!(self.Notification && self.Notification.permission === 'granted')) {
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
      }
    }
  }

  if (payload.title == null) {
    payload.title = 'City service';
  }

  event.waitUntil(
    self.registration.showNotification(payload.title, payload.options)
  );
});

self.addEventListener('notificationclick', (event) => {
  var notification = event.notification;
  notification.close();

  if (notification.data != null && notification.data.url) {
    clients.openWindow(notification.data.url);
  }
});