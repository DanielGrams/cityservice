<template>
  <div>
    <b-overlay :show="isLoading">
      <div v-if="place">
        <h3 class="d-flex justify-content-between align-items-center">
          <span>{{ place.name }}</span>
          <b-button-group v-if="currentUser" class="pr-2">
            <b-button
              @click="toggleFavorite()"
              class="favorite-btn"
              variant="secondary"
              ><b-icon :icon="place.is_favored ? 'star-fill' : 'star'"></b-icon
            ></b-button>
          </b-button-group>
        </h3>
      </div>
      <NewsList />
    </b-overlay>
  </div>
</template>

<script>
import axios from "axios";
import NewsList from "../components/NewsList.vue";

export default {
  components: {
    NewsList,
  },
  data() {
    return {
      isLoading: false,
      place: null,
    };
  },
  computed: {
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
      axios
        .get(`/api/places/${this.$route.params.id}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.place = response.data;
        });
    },
    toggleFavorite() {
      if (this.place.is_favored) {
        axios.delete(`/api/user/places/${this.place.id}`).then(() => {
          this.place.is_favored = false;
        });
      } else {
        axios.put(`/api/user/places/${this.place.id}`).then(() => {
          this.place.is_favored = true;
        });
      }
    },
  },
};
</script>
