<template>
  <div>
    <b-overlay :show="isLoading">
      <div v-if="place">
        <b-button-group class="my-4">
          <b-button
            @click="$refs.update.showModal()"
            class="edit-btn"
            variant="light"
            ><b-icon icon="pencil-fill"></b-icon
          ></b-button>
          <b-button @click="deleteItem" variant="light" class="delete-btn"
            ><b-icon icon="trash-fill"></b-icon
          ></b-button>
        </b-button-group>
        <div class="my-4"></div>

        <Update ref="update" :id="$route.params.id" @updated="loadData" />

        <h3>{{ place.name }}</h3>
        <b-table stacked :fields="propertyFields" :items="properties">
        </b-table>
      </div>
    </b-overlay>
  </div>
</template>

<script>
import axios from "axios";
import Update from "../components/Update.vue";

export default {
  components: { Update },
  computed: {
    properties() {
      return [this.place];
    },
  },
  data() {
    return {
      isLoading: false,
      place: null,
      propertyFields: [
        {
          key: "recycling_ids",
          label: this.$t("app.admin.places.recyclingIds"),
        },
        {
          key: "weather_warning_name",
          label: this.$t("app.admin.places.weatherWarningName"),
        },
      ],
    };
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
    deleteItem() {
      if (confirm(this.$t("app.admin.places.deleteConfirmation"))) {
        axios.delete(`/api/places/${this.$route.params.id}`).then(() => {
          this.$root.makeSuccessToast(
            this.$t("app.admin.places.deletedMessage")
          );
          this.$root.goBack(`/admin/places`);
        });
      }
    },
  },
};
</script>
