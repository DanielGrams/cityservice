import Vue from "vue";
import App from "./App.vue";
import router from "./app/router";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import moment from "moment";
import VueMoment from "vue-moment";
import VueMeta from "vue-meta";
import * as VeeValidate from "vee-validate";
import VueCookies from "vue-cookies";
import axios from "axios";
import Vlf from 'vlf'
import localforage from 'localforage'
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import * as rules from "vee-validate/dist/rules";
import { messages } from "vee-validate/dist/locale/de.json";

import "./custom.scss";
import i18n from "./i18n";
import store from "./store";
import './registerServiceWorker'

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

var vue = new Vue({
  router,
  i18n,
  store,
  render: (h) => h(App),
  methods: {
    handleAxiosStart(config) {
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
    handleAxiosFinish(config) {
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
    handleAxiosError(error) {
      if (error && error.config) {
        this.handleAxiosFinish(error.config);
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
  },
}).$mount("#app");

axios.defaults.withCredentials = true;
axios.interceptors.request.use(
  function (config) {
    if (config) {
      vue.handleAxiosStart(config);
    }
    return config;
  },
  /* istanbul ignore next */
  function (error) {
    vue.handleAxiosError(error);
    return Promise.reject(error);
  }
);
axios.interceptors.response.use(
  function (response) {
    if (response && response.config) {
      vue.handleAxiosFinish(response.config);
    }
    return response;
  },
  function (error) {
    vue.handleAxiosError(error);
    return Promise.reject(error);
  }
);
