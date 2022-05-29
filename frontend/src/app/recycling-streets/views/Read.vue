<template>
  <div>
    <b-overlay :show="isLoading">
      <div v-if="recyclingStreet">
        <h3 class="d-flex justify-content-between align-items-center">
          <div>
            <BackButton path="/places" />
            <span>{{ recyclingStreet.name }}</span>
          </div>
          <b-button-group v-if="currentUser" class="pr-2">
            <b-button
              @click="toggleFavorite()"
              class="favorite-btn"
              variant="light"
              ><b-icon
                :icon="recyclingStreet.is_favored ? 'star-fill' : 'star'"
              ></b-icon
            ></b-button>
          </b-button-group>
        </h3>
      </div>
      <RecyclingEventList />
    </b-overlay>
  </div>
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
