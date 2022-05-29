import httpService from "@/services/http.service";
import { Capacitor } from "@capacitor/core";
import { PushNotifications } from "@capacitor/push-notifications";
import { Storage } from "@capacitor/storage";

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
      return PushNotifications.checkPermissions().then((result) => {
        return Promise.resolve(result.receive);
      });
    }

    return Promise.resolve(Notification.permission);
  }

  savePushRegistrationToStorage(pushRegistrationId, token) {
    const pushInfo = {
      pushRegistrationId: pushRegistrationId,
      token: token,
    };

    return Storage.set({
      key: "pushInfo",
      value: JSON.stringify(pushInfo),
    });
  }

  deletePushRegistrationFromStorage() {
    return Storage.remove({ key: "pushInfo" });
  }

  handlePushLoaded(pushRegistrationId, token) {
    return Storage.get({ key: "pushInfo" }).then(({ pushInfo }) => {
      if (!pushInfo) {
        return this.savePushRegistrationToStorage(pushRegistrationId, token);
      }

      return this.handlePushUpdate(pushInfo);
    });
  }

  handlePushUpdate(pushInfo, newToken) {
    if (pushInfo.token == newToken) {
      return Promise.resolve();
    }

    return this.updatePushRegistration(
      pushInfo.pushRegistrationId,
      newToken
    ).then(() => {
      return this.savePushRegistrationToStorage(
        pushInfo.pushRegistrationId,
        newToken
      );
    });
  }

  loadPushRegistration(token) {
    return httpService
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
    return httpService
      .post("/api/user/push-registrations", pushRegistration)
      .then((response) => {
        if (response.status == 201) {
          return response.data.id;
        }

        return null;
      });
  }

  updatePushRegistration(pushRegistrationId, token) {
    return httpService.patch(
      `/api/user/push-registrations/${pushRegistrationId}`,
      {
        token: token,
      }
    );
  }

  deletePushRegistration(pushRegistrationId) {
    return httpService.delete(
      `/api/user/push-registrations/${pushRegistrationId}`
    );
  }

  sendTestNotification(pushRegistrationId) {
    return httpService.post(
      `/api/user/push-registrations/${pushRegistrationId}/send`
    );
  }
}

export default new NotificationService();
