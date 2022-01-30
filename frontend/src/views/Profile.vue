<template>
  <div class="container" v-if="currentUser">
    <h3>{{ $t("profile.title") }}</h3>
    <p>
      {{ currentUser.email }}
    </p>
    <ul>
      <li v-for="(role, index) in currentUser.roles" :key="index">
        {{ role }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Profile",
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push({ name: "Login" });
    }
  },
};
</script>
