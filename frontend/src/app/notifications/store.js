import i18n from "@/i18n";
import NotificationService from "../../services/notification.service";

/* istanbul ignore next */
export const notifications = {
  namespaced: true,
  state: {
    notificationsSupported: false,
    notificationPermission: null,
    subscription: null,
    pushRegistrationId: null,
    initialized: false,
    initializing: false,
    registering: false,
  },
  getters: {
    notificationsSupported: (state) => {
      return state.notificationsSupported;
    },
    permissionGranted: (state) => {
      return state.notificationPermission === "granted";
    },
  },
  actions: {
    init({ commit, getters }) {
      const supported =
        "Notification" in window &&
        "PushManager" in window &&
        navigator.serviceWorker != null;
      const permission = Notification.permission;
      commit("initStart", { supported: supported, permission: permission });

      if (!supported || !getters.permissionGranted) {
        commit("initFinish", { subscription: null, pushRegistrationId: null });
        return;
      }

      return navigator.serviceWorker.ready.then((reg) => {
        if (reg.pushManager == null) {
          commit("initFinish", {
            subscription: null,
            pushRegistrationId: null,
          });
          return;
        }

        return reg.pushManager.getSubscription().then((subscription) => {
          if (subscription == null) {
            commit("initFinish", {
              subscription: null,
              pushRegistrationId: null,
            });
            return;
          }

          return NotificationService.loadPushRegistration(subscription).then(
            (pushRegistrationId) => {
              commit("initFinish", {
                subscription: subscription,
                pushRegistrationId: pushRegistrationId,
              });
              reg.active.postMessage({
                action: "PUSH_LOADED",
                pushRegistrationId: pushRegistrationId,
                subscription: JSON.parse(JSON.stringify(subscription)),
              });
            },
            () => {
              commit("initFinish", {
                subscription: subscription,
                pushRegistrationId: null,
              });
              reg.active.postMessage({
                action: "PUSH_UNREGISTERED",
              });
            }
          );
        });
      });
    },
    registerPush({ commit }) {
      commit("registerStart");

      return Notification.requestPermission(() => {
        const permission = Notification.permission;

        if (permission != "granted") {
          commit("registerFinish", {
            permission: permission,
            subscription: null,
            pushRegistrationId: null,
          });
          return Promise.reject(
            new Error(i18n.t("app.notifications.permissionDenied"))
          );
        }

        return navigator.serviceWorker.ready.then((reg) => {
          if (reg.pushManager == null) {
            commit("registerFinish", {
              permission: permission,
              subscription: null,
              pushRegistrationId: null,
            });
            return Promise.reject(
              new Error(i18n.t("app.notifications.notSupported"))
            );
          }

          return reg.pushManager
            .subscribe({
              userVisibleOnly: true,
              applicationServerKey: process.env.VUE_APP_VAPID_SERVER_KEY,
            })
            .then((subscription) => {
              const pushRegistration = {
                device: window.navigator.userAgent,
                platform: "web",
                token: JSON.stringify(subscription),
              };

              return NotificationService.addPushRegistration(
                pushRegistration
              ).then(
                (pushRegistrationId) => {
                  commit("registerFinish", {
                    permission: permission,
                    subscription: subscription,
                    pushRegistrationId: pushRegistrationId,
                  });
                  reg.active.postMessage({
                    action: "PUSH_REGISTERED",
                    pushRegistrationId: pushRegistrationId,
                    subscription: JSON.parse(JSON.stringify(subscription)),
                  });
                  return Promise.resolve();
                },
                (error) => {
                  commit("registerFinish", {
                    permission: permission,
                    subscription: subscription,
                    pushRegistrationId: null,
                  });
                  return Promise.resolve(error);
                }
              );
            });
        });
      });
    },
    unregisterPush({ commit, dispatch, state }) {
      commit("unregisterStart");
      navigator.serviceWorker.ready.then((registration) => {
        registration.active.postMessage({
          action: "PUSH_UNREGISTERED",
        });
      });
      dispatch("deletePushRegistration", {
        pushRegistrationId: state.pushRegistrationId,
      });

      return navigator.serviceWorker.ready.then((reg) => {
        reg.pushManager.getSubscription().then((subscription) => {
          if (subscription != null) {
            subscription.unsubscribe();
          }
        });
      });
    },
    deletePushRegistration({ commit, state }, { pushRegistrationId }) {
      return NotificationService.deletePushRegistration(
        pushRegistrationId
      ).then(
        () => {
          commit("deletePushRegistration", { pushRegistrationId });

          if (state.pushRegistrationId == pushRegistrationId) {
            navigator.serviceWorker.ready.then((registration) => {
              registration.active.postMessage({
                action: "PUSH_UNREGISTERED",
              });
            });
          }

          return Promise.resolve();
        },
        (error) => {
          return Promise.reject(error);
        }
      );
    },
    sendTestNotification({ state }) {
      return NotificationService.sendTestNotification(state.pushRegistrationId);
    },
  },
  mutations: {
    initStart(state, { supported, permission }) {
      state.initializing = true;
      state.notificationsSupported = supported;
      state.notificationPermission = permission;
    },
    initFinish(state, { subscription, pushRegistrationId }) {
      state.initializing = false;
      state.initialized = true;
      state.subscription = subscription;
      state.pushRegistrationId = pushRegistrationId;
    },
    registerStart(state) {
      state.registering = true;
    },
    registerFinish(state, { permission, subscription, pushRegistrationId }) {
      state.registering = false;
      state.notificationPermission = permission;
      state.subscription = subscription;
      state.pushRegistrationId = pushRegistrationId;
    },
    deletePushRegistration(state, { pushRegistrationId }) {
      if (state.pushRegistrationId == pushRegistrationId) {
        state.pushRegistrationId = null;
      }
    },
  },
};
