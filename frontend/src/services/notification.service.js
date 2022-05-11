import axios from "axios";
import { Capacitor } from "@capacitor/core";
import { PushNotifications } from "@capacitor/push-notifications";

/* istanbul ignore next */
class NotificationService {
  areNotificationsSupported() {
    if (Capacitor.isNativePlatform()) {
      return Capacitor.isPluginAvailable("PushNotifications");
    }

    return (
      "Notification" in window &&
      "PushManager" in window &&
      navigator.serviceWorker != null
    );
  }

  getPermission() {
    if (Capacitor.isNativePlatform()) {
      return PushNotifications.checkPermissions().then((result => {
        return Promise.resolve(result.receive);
      }));
    }

    return Promise.resolve(Notification.permission);
  }

  loadPushRegistration(token) {
    return axios
      .get(`/api/user/push-registrations?token=${encodeURIComponent(token)}`, {
        suppressErrorToast: true,
      })
      .then((response) => {
        if (response.data.items.length > 0) {
          return response.data.items[0].id;
        }

        return null;
      });
  }

  addPushRegistration(pushRegistration) {
    return axios
      .post("/api/user/push-registrations", pushRegistration)
      .then((response) => {
        if (response.status == 201) {
          return response.data.id;
        }

        return null;
      });
  }

  deletePushRegistration(pushRegistrationId) {
    return axios.delete(`/api/user/push-registrations/${pushRegistrationId}`);
  }

  sendTestNotification(pushRegistrationId) {
    return axios.post(
      `/api/user/push-registrations/${pushRegistrationId}/send`
    );
  }
}

export default new NotificationService();
