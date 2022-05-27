import Vue from "vue";
import App from "./App.vue";
import router from "./app/router";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import moment from "moment";
import VueMoment from "vue-moment";
import VueMeta from "vue-meta";
import * as VeeValidate from "vee-validate";
import VueCookies from "vue-cookies";
import Vlf from "vlf";
import localforage from "localforage";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import * as rules from "vee-validate/dist/rules";
import { messages } from "vee-validate/dist/locale/de.json";
import { Capacitor } from "@capacitor/core";
import { PushNotifications } from "@capacitor/push-notifications";
import { Browser } from "@capacitor/browser";
import { Dialog } from "@capacitor/dialog";
import { App as NativeApp } from '@capacitor/app';
import "./custom.scss";
import i18n from "./i18n";
import store from "./store";
import httpService from "./services/http.service";
import "./registerServiceWorker";

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VeeValidate);
Vue.use(VueCookies);
Vue.use(Vlf, localforage);

require("moment/locale/de");
moment.locale("de");
Vue.use(VueMoment, { moment });

Vue.$cookies.config("7d");

Vue.use(VueMeta, {
  refreshOnceOnNavigation: true,
});

Vue.component("ValidationProvider", ValidationProvider);
Vue.component("ValidationObserver", ValidationObserver);

Object.keys(rules).forEach((rule) => {
  extend(rule, {
    ...rules[rule],
    message: messages[rule],
  });
});

VeeValidate.extend("url", {
  validate: (value) => {
    if (value) {
      return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([-.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(
        value
      );
    }

    /* istanbul ignore next */
    return false;
  },
});

if ("VUE_APP_BASE_URL" in process.env) {
  httpService.baseURL = process.env.VUE_APP_BASE_URL;
}

var vue = new Vue({
  router,
  i18n,
  store,
  render: (h) => h(App),
  methods: {
    handleHttpStart(config) {
      /* istanbul ignore next */
      if (
        config &&
        Object.prototype.hasOwnProperty.call(config, "handleRequestStart")
      ) {
        config.handleRequestStart();
      }

      /* istanbul ignore next */
      if (
        config &&
        Object.prototype.hasOwnProperty.call(config, "handleLoading")
      ) {
        config.handleLoading(true);
      }
    },
    handleHttpFinish(config) {
      /* istanbul ignore next */
      if (
        config &&
        Object.prototype.hasOwnProperty.call(config, "handleRequestFinish")
      ) {
        config.handleRequestFinish();
      }

      /* istanbul ignore next */
      if (
        config &&
        Object.prototype.hasOwnProperty.call(config, "handleLoading")
      ) {
        config.handleLoading(false);
      }
    },
    handleHttpError(error) {
      if (error && error.config) {
        this.handleHttpFinish(error.config);
      }

      const hasHandler =
        error.config &&
        Object.prototype.hasOwnProperty.call(
          error.config,
          "handleRequestError"
        );

      error.config = {
        suppressErrorToast: false,
        ...(error.config || {}),
      };

      if (!hasHandler && error.config.suppressErrorToast) {
        return;
      }

      /* istanbul ignore next */
      const status = error && error.response && error.response.status;
      /* istanbul ignore next */
      let message = error.message || error;

      /* istanbul ignore next */
      if (status == 400 || status == 422) {
        message =
          (error &&
            error.response &&
            error.response.data &&
            error.response.data.message) ||
          error;
        const errorName =
          error &&
          error.response &&
          error.response.data &&
          error.response.data.name;

        if (errorName == "Unique Violation") {
          message = this.$t("shared.errors.uniqueViolation");
        } else if (errorName == "Unprocessable Entity") {
          message = this.$t("shared.errors.unprocessableEntity");
        }
      }

      /* istanbul ignore next */
      if (hasHandler) {
        error.config.handleRequestError(error, message);
      } /* istanbul ignore next */ else {
        this.makeErrorToast(message);
      }
    },
    makeErrorToast(message) {
      this.makeToast(message, "danger", this.$t("shared.toast.errorTitle"));
    },
    /* istanbul ignore next */
    makeSuccessToast(message) {
      this.makeToast(message, "success", this.$t("shared.toast.successTitle"));
    },
    makeToast(message, variant, title) {
      this.$bvToast.toast(message, {
        title: title,
        variant: variant,
        toaster: "b-toaster-top-center",
        noCloseButton: true,
        solid: true,
      });
    },
    /* istanbul ignore next */
    goBack(fallbackPath) {
      window.history.length > 1
        ? this.$router.go(-1)
        : this.$router.push({ path: fallbackPath });
    },
    openURL(originalURL) {
      let url = originalURL;

      if (url.startsWith(httpService.baseURL)) {
        url = url.replace(httpService.baseURL, "");
      }

      console.log("openURL", url);
      const resolved = router.resolve(url);
      console.log("resolved", resolved);
      if (resolved.route.name != "NotFound") {
        router.push(resolved.route);
      } else {
        Browser.open({ url: originalURL });
      }
    },
  },
}).$mount("#app");

httpService.handler = vue;

/* istanbul ignore next */
if (Capacitor.isPluginAvailable("PushNotifications")) {
  PushNotifications.addListener("registration", (token) => {
    PushNotifications.removeAllDeliveredNotifications();
    store
      .dispatch("notifications/handleRegistration", { token: token.value })
      .then(
        () => {
          if (store.state.notifications.registerAction == "registerPush") {
            vue.makeSuccessToast(
              i18n.t("app.user.profile.pushRegistrations.addedMessage")
            );
          }
        },
        (error) => {
          if (store.state.notifications.registerAction == "registerPush") {
            vue.makeErrorToast(error.message);
          }
        }
      );
  });

  PushNotifications.addListener("registrationError", (error) => {
    console.error("registrationError", JSON.stringify(error));
    store.dispatch("notifications/handleRegistrationError");
    vue.makeErrorToast(error.message);
  });

  PushNotifications.addListener("pushNotificationReceived", (notification) => {
    PushNotifications.removeAllDeliveredNotifications();

    const title = notification.title || "City service";
    const url = notification.data && notification.data.url;

    if (url == null) {
      Dialog.alert({
        title: title,
        message: notification.body,
      });
      return;
    }

    Dialog.confirm({
      title: title,
      message: notification.body,
    }).then((result) => {
      if (result.value) {
        vue.openURL(url);
      }
    });
  });

  PushNotifications.addListener("pushNotificationActionPerformed", (action) => {
    const notification = action.notification;
    const url = notification.data && notification.data.url;

    if (url != null) {
      vue.openURL(url);
    }
  });
}

/* istanbul ignore next */
if (Capacitor.isPluginAvailable("App")) {
  NativeApp.addListener("appStateChange", (state) => {
    if (state.isActive) {
      if (Capacitor.isPluginAvailable("PushNotifications")) {
        // TODO dgr: Nur machen, wenn Push registriert ist
        PushNotifications.removeAllDeliveredNotifications();
      }
    }
  });
}
