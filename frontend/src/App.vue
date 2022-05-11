<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light">
      <b-navbar-brand to="/">
        <img
          src="@/assets/apple-touch-icon.png"
          width="30"
          height="30"
          class="d-inline-block align-top rounded"
          alt="Logo"
        />
        {{ $t("app.menu.title") }}
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/places">{{ $t("app.menu.places") }}</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav v-if="currentUser">
          <b-nav-item to="/user/profile">{{
            $t("app.menu.profile")
          }}</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item v-if="!currentUser" to="/login">{{
            $t("app.menu.login")
          }}</b-nav-item>
          <b-nav-item-dropdown v-if="currentUser" right class="user-dropdown">
            <template #button-content>
              {{ currentUser.email }}
            </template>
            <b-dropdown-item v-if="isAdmin" to="/admin">{{
              $t("app.menu.admin")
            }}</b-dropdown-item>
            <b-dropdown-item class="logout" href @click.prevent="logOut">{{
              $t("app.menu.logout")
            }}</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
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

    <div class="body-content">
      <router-view />
      <footer>
        <p class="text-center">
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
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    isAdmin() {
      return this.$store.getters["auth/isAdmin"];
    },
  },
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
    logOut() {
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.replace("/");
      });
    },
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
