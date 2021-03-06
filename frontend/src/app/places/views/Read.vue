<template>
  <DefaultPage :title="title">
    <template #left>
      <BackButton path="/places" />
    </template>
    <template #right>
      <b-button-group v-if="currentUser && place" class="pr-2">
        <b-button @click="toggleFavorite()" class="favorite-btn" variant="light"
          ><b-icon :icon="place.is_favored ? 'star-fill' : 'star'"></b-icon
        ></b-button>
      </b-button-group>
    </template>
    <template>
      <b-overlay :show="isLoading">
        <b-nav tabs class="tabs">
          <b-nav-item
            :to="`/places/${this.placeId}`"
            exact
            exact-active-class="active"
            replace
            >{{ $t("app.places.read.news.title") }}</b-nav-item
          >
          <b-nav-item
            :to="`/places/${this.placeId}/weather`"
            exact
            exact-active-class="active"
            replace
            >{{ $t("app.places.read.weather.title") }}</b-nav-item
          >
          <b-nav-item
            :to="`/places/${this.placeId}/recycling`"
            exact
            exact-active-class="active"
            replace
            >{{ $t("app.places.read.recycling.title") }}</b-nav-item
          >
        </b-nav>

        <router-view></router-view>
      </b-overlay>
    </template>
  </DefaultPage>
</template>

<script>
import httpService from "@/services/http.service";
import BackButton from "@/components/BackButton.vue";

export default {
  components: { BackButton },
  data() {
    return {
      isLoading: false,
      place: null,
    };
  },
  computed: {
    title() {
      return this.place ? this.place.name : "";
    },
    placeId() {
      return this.$route.params.id;
    },
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    this.isLoading = false;
    this.place = null;
    this.loadData();
  },
  methods: {
    loadData() {
      httpService
        .get(`/api/places/${this.placeId}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.place = response.data;
        });
    },
    toggleFavorite() {
      if (this.place.is_favored) {
        httpService.delete(`/api/user/places/${this.place.id}`).then(() => {
          this.place.is_favored = false;
        });
      } else {
        httpService.put(`/api/user/places/${this.place.id}`).then(() => {
          this.place.is_favored = true;
        });
      }
    },
  },
};
</script>
