import i18n from "@/i18n";
import NotificationService from "../../services/notification.service";
import { Capacitor } from "@capacitor/core";
import { PushNotifications } from "@capacitor/push-notifications";
import { Device } from "@capacitor/device";

/* istanbul ignore next */
export const notifications = {
  namespaced: true,
  state: {
    notificationsSupported: false,
    notificationPermission: null,
    token: null,
    pushRegistrationId: null,
    initialized: false,
    initializing: false,
    registering: false,
    registerAction: null,
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
    init({ commit }) {
      const supported = NotificationService.areNotificationsSupported();
      commit("initStart", { supported: supported });

      if (!supported) {
        commit("initFinish", {
          permission: null,
          token: null,
          pushRegistrationId: null,
        });
        return;
      }

      return NotificationService.getPermission().then((permission) => {
        if (permission !== "granted") {
          commit("initFinish", {
            permission: permission,
            token: null,
            pushRegistrationId: null,
          });
          return;
        }

        if (Capacitor.isNativePlatform()) {
          commit("setRegisterAction", { action: "init" });
          PushNotifications.register();
          // Continues in PushNotifications.addListener("registration"|"registrationError")
          return;
        }

        return navigator.serviceWorker.ready.then((reg) => {
          if (reg.pushManager == null) {
            commit("initFinish", {
              permission: permission,
              token: null,
              pushRegistrationId: null,
            });
            return;
          }

          return reg.pushManager.getSubscription().then((subscription) => {
            if (subscription == null) {
              commit("initFinish", {
                permission: permission,
                token: null,
                pushRegistrationId: null,
              });
              return;
            }

            const token = JSON.stringify(subscription);
            return NotificationService.loadPushRegistration(token).then(
              (pushRegistrationId) => {
                commit("initFinish", {
                  permission: permission,
                  token: token,
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
                  permission: permission,
                  token: token,
                  pushRegistrationId: null,
                });
                reg.active.postMessage({
                  action: "PUSH_UNREGISTERED",
                });
              }
            );
          });
        });
      });
    },
    registerPush({ commit }) {
      commit("registerStart");

      if (Capacitor.isNativePlatform()) {
        return PushNotifications.requestPermissions().then((result) => {
          if (result.receive != "granted") {
            commit("registerFinish", {
              permission: result.receive,
              token: null,
              pushRegistrationId: null,
            });
            return Promise.reject(
              new Error(i18n.t("app.notifications.permissionDenied"))
            );
          }

          // Continues in PushNotifications.addListener("registration"|"registrationError")
          commit("setRegisterAction", { action: "registerPush" });
          PushNotifications.register();
          return Promise.resolve(true);
        });
      }

      return Notification.requestPermission(() => {
        const permission = Notification.permission;

        if (permission != "granted") {
          commit("registerFinish", {
            permission: permission,
            token: null,
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
              token: null,
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
              const token = JSON.stringify(subscription);
              const pushRegistration = {
                device: window.navigator.userAgent,
                platform: "web",
                token: token,
              };

              return NotificationService.addPushRegistration(
                pushRegistration
              ).then(
                (pushRegistrationId) => {
                  commit("registerFinish", {
                    permission: permission,
                    token: token,
                    pushRegistrationId: pushRegistrationId,
                  });
                  reg.active.postMessage({
                    action: "PUSH_REGISTERED",
                    pushRegistrationId: pushRegistrationId,
                    subscription: JSON.parse(JSON.stringify(subscription)),
                  });
                  return Promise.resolve(false);
                },
                (error) => {
                  commit("registerFinish", {
                    permission: permission,
                    token: token,
                    pushRegistrationId: null,
                  });
                  return Promise.reject(error);
                }
              );
            });
        });
      });
    },
    handleRegistration({ commit, state }, { token }) {
      const permission = "granted";
      if (state.registerAction == "init") {
        return NotificationService.loadPushRegistration(token).then(
          (pushRegistrationId) => {
            commit("initFinish", {
              permission: permission,
              token: token,
              pushRegistrationId: pushRegistrationId,
            });

            NotificationService.handlePushLoaded(pushRegistrationId, token);
          },
          () => {
            commit("initFinish", {
              permission: permission,
              token: token,
              pushRegistrationId: null,
            });

            NotificationService.deletePushRegistrationFromStorage();
          }
        );
      } else if (state.registerAction == "registerPush") {
        return Device.getInfo().then((deviceInfo) => {
          const pushRegistration = {
            device: (
              deviceInfo.name +
              " " +
              deviceInfo.manufacturer +
              " " +
              deviceInfo.model
            ).trim(),
            platform: deviceInfo.platform,
            token: token,
          };

          return NotificationService.addPushRegistration(pushRegistration).then(
            (pushRegistrationId) => {
              commit("registerFinish", {
                permission: permission,
                token: token,
                pushRegistrationId: pushRegistrationId,
              });

              return NotificationService.savePushRegistrationToStorage(
                pushRegistrationId,
                token
              );
            },
            (error) => {
              commit("registerFinish", {
                permission: permission,
                token: token,
                pushRegistrationId: null,
              });
              return Promise.resolve(error);
            }
          );
        });
      }
    },
    handleRegistrationError({ commit, state }) {
      const permission = "granted";
      if (state.registerAction == "init") {
        commit("initFinish", {
          permission: permission,
          token: null,
          pushRegistrationId: null,
        });
      } else if (state.registerAction == "registerPush") {
        commit("registerFinish", {
          permission: permission,
          token: null,
          pushRegistrationId: null,
        });
      }
    },
    unregisterPush({ dispatch, state }) {
      if (Capacitor.isNativePlatform()) {
        dispatch("deletePushRegistration", {
          pushRegistrationId: state.pushRegistrationId,
        });
        return;
      }

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
    initStart(state, { supported }) {
      state.initializing = true;
      state.notificationsSupported = supported;
    },
    initFinish(state, { permission, token, pushRegistrationId }) {
      state.notificationPermission = permission;
      state.initializing = false;
      state.initialized = true;
      state.token = token;
      state.pushRegistrationId = pushRegistrationId;
    },
    registerStart(state) {
      state.registering = true;
    },
    registerFinish(state, { permission, token, pushRegistrationId }) {
      state.registering = false;
      state.notificationPermission = permission;
      state.token = token;
      state.pushRegistrationId = pushRegistrationId;
    },
    deletePushRegistration(state, { pushRegistrationId }) {
      if (state.pushRegistrationId == pushRegistrationId) {
        state.pushRegistrationId = null;
      }
    },
    setRegisterAction(state, { action }) {
      state.registerAction = action;
    },
  },
};
