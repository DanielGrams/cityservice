<template>
  <div class="container" v-if="currentUser">
    <h3>{{ $t("app.user.profile.title") }}</h3>
    <p>
      {{ currentUser.email }}
    </p>

    <UserPlaceList />
    <UserRecyclingStreetList />
  </div>
</template>

<script>
import UserPlaceList from "../components/UserPlaceList.vue";
import UserRecyclingStreetList from "../components/UserRecyclingStreetList.vue";
export default {
  components: { UserPlaceList, UserRecyclingStreetList },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
};
</script>
