<template>
  <DefaultPage :title="$t('app.user.home.title')">
    <div>
      <RecyclingEventList />
      <b-overlay :show="isLoading">
        <Place v-for="place in places" :key="place.id" :place="place" />
      </b-overlay>
    </div>
  </DefaultPage>
</template>

<script>
import httpService from "@/services/http.service";
import Place from "../components/Place.vue";
import RecyclingEventList from "../components/RecyclingEventList.vue";
import DefaultPage from "@/components/DefaultPage";

export default {
  components: {
    DefaultPage,
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
