<template>
  <div>
    <b-overlay :show="isLoading">
      <div v-if="recyclingStreet">
        <h3 class="d-flex justify-content-between align-items-center">
          <span>{{ recyclingStreet.name }}</span>
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
import axios from "axios";
import RecyclingEventList from "../components/RecyclingEventList.vue";

export default {
  components: {
    RecyclingEventList,
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
      axios
        .get(`/api/recycling-streets/${this.$route.params.id}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.recyclingStreet = response.data;
        });
    },
    toggleFavorite() {
      if (this.recyclingStreet.is_favored) {
        axios
          .delete(`/api/user/recycling-streets/${this.recyclingStreet.id}`)
          .then(() => {
            this.recyclingStreet.is_favored = false;
          });
      } else {
        axios
          .put(`/api/user/recycling-streets/${this.recyclingStreet.id}`)
          .then(() => {
            this.recyclingStreet.is_favored = true;
          });
      }
    },
  },
};
</script>
