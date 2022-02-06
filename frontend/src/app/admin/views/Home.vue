<template>
  <div class="container" v-if="currentUser">
    <h3>{{ $t("app.admin.home.title") }}</h3>
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
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
};
</script>
