<template>
  <div class="container" v-if="currentUser">
    <h3>{{ $t("app.user.profile.title") }}</h3>
    <p>
      {{ currentUser.email }}
      <b-button variant="link" class="logout" @click.prevent="logOut">{{
        $t("app.menu.logout")
      }}</b-button>
      <b-button variant="link" class="admin" v-if="isAdmin" to="/admin">{{
        $t("app.menu.admin")
      }}</b-button>
    </p>

    <UserPlaceList />
    <UserRecyclingStreetList />
    <UserPushRegistrationList />
  </div>
</template>

<script>
import UserPlaceList from "../components/UserPlaceList.vue";
import UserRecyclingStreetList from "../components/UserRecyclingStreetList.vue";
import UserPushRegistrationList from "../components/UserPushRegistrationList.vue";

export default {
  components: {
    UserPlaceList,
    UserRecyclingStreetList,
    UserPushRegistrationList,
  },
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
