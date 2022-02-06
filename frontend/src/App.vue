<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light">
      <b-navbar-brand href="/">
        <img
          src="@/assets/apple-touch-icon.png"
          width="30"
          height="30"
          class="d-inline-block align-top rounded"
          alt="Logo"
        />
        {{ $t("app.title") }}
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/news">{{ $t("app.menu.news") }}</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item v-if="!currentUser" to="/login">{{
            $t("app.menu.login")
          }}</b-nav-item>
          <b-nav-item-dropdown v-if="currentUser" right class="user-dropdown">
            <template #button-content>
              {{ currentUser.email }}
            </template>
            <b-dropdown-item to="/user/profile">{{
              $t("app.menu.profile")
            }}</b-dropdown-item>
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

    <div class="body-content">
      <router-view />
      <footer>
        <p class="text-center">
          <i18n path="app.withLove" tag="span">
            <template v-slot:love>
              <b-icon icon="heart-fill" style="color: red"></b-icon>
            </template>
            <template v-slot:place>
              <strong>Goslar</strong>
            </template>
          </i18n>
        </p>
        <p class="text-center small">
          <a href="/impressum">{{ $t("app.footer.imprint") }}</a> &vert;
          <a href="/impressum">{{ $t("app.footer.contact") }}</a> &vert;
          <a href="/datenschutz">{{ $t("app.footer.privacy") }}</a>
        </p>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    isAdmin() {
      return this.$store.getters["auth/isAdmin"];
    },
  },
  methods: {
    logOut() {
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.replace("/");
      });
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
