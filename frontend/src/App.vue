<template>
  <div id="app">
    <b-navbar type="light" fixed="bottom" variant="light">
      <b-navbar-nav justified class="col col-md-6 m-md-auto">
        <b-nav-item to="/">
          <b-icon icon="house-door-fill"></b-icon>
          <div class="small">{{ $t("app.menu.home") }}</div>
        </b-nav-item>
        <b-nav-item to="/places">
          <b-icon icon="search"></b-icon>
          <div class="small">{{ $t("app.menu.places") }}</div>
        </b-nav-item>
        <b-nav-item to="/user/profile">
          <b-icon icon="person-fill"></b-icon>
          <div class="small">{{ $t("app.menu.profile") }}</div>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <b-alert
      v-model="isRefresh"
      class="position-fixed fixed-bottom m-0 rounded-0"
      style="z-index: 2000"
      variant="info"
    >
      <div class="mb-2">{{ $t("app.updateAlert.message") }}</div>
      <b-button variant="info" @click="update">{{
        $t("app.updateAlert.button")
      }}</b-button>
    </b-alert>

    <div class="body-content mb-5">
      <router-view />
      <footer class="mt-5">
        <p class="text-center small text-center text-secondary mb-1">
          <i18n path="app.footer.withLove" tag="span">
            <template v-slot:love>
              <b-icon icon="heart-fill" style="color: red"></b-icon>
            </template>
            <template v-slot:place>
              <strong>Goslar</strong>
            </template>
          </i18n>
        </p>
        <p class="text-center small">
          <b-link to="/impressum">{{ $t("app.footer.imprint") }}</b-link> &vert;
          <b-link to="/impressum">{{ $t("app.footer.contact") }}</b-link> &vert;
          <b-link to="/datenschutz">{{ $t("app.footer.privacy") }}</b-link>
        </p>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  metaInfo: {
    title: "City Service App",
  },
  data: () => ({
    registration: null,
    isRefresh: false,
    refreshing: false,
  }),
  created() {
    document.addEventListener("serviceWorkerUpdateEvent", this.appUpdateUI, {
      once: true,
    });

    /* istanbul ignore next */
    if (navigator.serviceWorker == null) {
      return;
    }

    // Prevent multiple refreshes
    /* istanbul ignore next */
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (this.refreshing) {
        return;
      }

      this.refreshing = true;
      // Here the actual reload of the page occurs
      window.location.reload();
    });
  },
  methods: {
    /* istanbul ignore next */
    appUpdateUI(e) {
      this.registration = e.detail;
      this.isRefresh = true;
    },
    /* istanbul ignore next */
    update() {
      this.isRefresh = false;

      // Make sure we only send a 'skip waiting' message if the SW is waiting
      if (!this.registration || !this.registration.waiting) {
        return;
      }

      // Send message to SW to skip the waiting and activate the new SW
      this.registration.waiting.postMessage({ type: "SKIP_WAITING" });
    },
  },
};
</script>

<style>
.navbar {
  background-color: lightslategray;
  font-size: 1em;
  font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
    "Lucida Sans", Arial, sans-serif;
  color: white;
  padding: 8px 5px 8px 5px;
}

.navbar a {
  text-decoration: none;
  color: inherit;
}

.navbar-brand {
  font-size: 1.2em;
  font-weight: 600;
}

.navbar-item {
  font-variant: small-caps;
  margin-left: 30px;
}
</style>
