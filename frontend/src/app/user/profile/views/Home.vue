<template>
  <div class="container" v-if="currentUser">
    <h3>{{ $t("app.user.profile.title") }}</h3>
    <p>
      {{ currentUser.email }}
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
  },
};
</script>
