<template>
  <div v-if="currentUser">
    <h3>{{ $t("app.admin.home.title") }}</h3>
    <p>
      {{ currentUser.email }}
    </p>
    <ul>
      <li v-for="(role, index) in currentUser.roles" :key="index">
        {{ role }}
      </li>
    </ul>
    <ul>
      <li>
        <b-link to="/admin/news-feeds">{{
          $t("app.admin.home.newsFeeds")
        }}</b-link>
      </li>
      <li>
        <b-link to="/admin/places">{{ $t("app.admin.home.places") }}</b-link>
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
