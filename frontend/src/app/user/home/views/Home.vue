<template>
  <div class="container">
    <h3>{{ $t("app.user.home.title") }}</h3>
    <RecyclingEventList />
    <b-overlay :show="isLoading">
      <Place v-for="place in places" :key="place.id" :place="place" />
    </b-overlay>
  </div>
</template>

<script>
import httpService from "@/services/http.service";
import Place from "../components/Place.vue";
import RecyclingEventList from "../components/RecyclingEventList.vue";

export default {
  components: {
    Place,
    RecyclingEventList,
  },
  data() {
    return {
      places: [],
      isLoading: false,
    };
  },
  mounted() {
    this.loadPlaces();
  },
  methods: {
    loadPlaces() {
      const vm = this;
      httpService
        .get(`/api/user/places`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          vm.places = response.data.items;
        });
    },
  },
};
</script>
