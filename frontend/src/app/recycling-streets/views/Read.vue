<template>
  <DefaultPage :title="title">
    <template #left>
      <BackButton path="/places" />
    </template>
    <template #right>
      <b-button-group v-if="currentUser && recyclingStreet" class="pr-2">
        <b-button @click="toggleFavorite()" class="favorite-btn" variant="light"
          ><b-icon
            :icon="recyclingStreet.is_favored ? 'star-fill' : 'star'"
          ></b-icon
        ></b-button>
      </b-button-group>
    </template>
    <template>
      <b-overlay :show="isLoading">
        <RecyclingEventList />
      </b-overlay>
    </template>
  </DefaultPage>
</template>

<script>
import httpService from "@/services/http.service";
import RecyclingEventList from "../components/RecyclingEventList.vue";
import BackButton from "@/components/BackButton.vue";

export default {
  components: {
    RecyclingEventList,
    BackButton,
  },
  data() {
    return {
      isLoading: false,
      recyclingStreet: null,
    };
  },
  computed: {
    title() {
      return this.recyclingStreet ? this.recyclingStreet.name : "";
    },
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    this.isLoading = false;
    this.recyclingStreet = null;
    this.loadData();
  },
  methods: {
    loadData() {
      httpService
        .get(`/api/recycling-streets/${this.$route.params.id}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.recyclingStreet = response.data;
        });
    },
    toggleFavorite() {
      if (this.recyclingStreet.is_favored) {
        httpService
          .delete(`/api/user/recycling-streets/${this.recyclingStreet.id}`)
          .then(() => {
            this.recyclingStreet.is_favored = false;
          });
      } else {
        httpService
          .put(`/api/user/recycling-streets/${this.recyclingStreet.id}`)
          .then(() => {
            this.recyclingStreet.is_favored = true;
          });
      }
    },
  },
};
</script>
