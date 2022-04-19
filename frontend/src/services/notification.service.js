import axios from "axios";

/* istanbul ignore next */
class NotificationService {
  loadPushRegistration(subscription) {
    const token = JSON.stringify(subscription);
    return axios
      .get(
        `/api/user/push-registrations?token=${encodeURIComponent(
          token
        )}`
      )
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
