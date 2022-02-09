<template>
  <div>
    <b-overlay :show="isLoading">
      <div v-if="newsFeed">
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

        <h3>{{ newsFeed.publisher }}</h3>
        <p>{{ newsFeed.url }}</p>
      </div>
    </b-overlay>
  </div>
</template>

<script>
import axios from "axios";
import Update from "../components/Update.vue";

export default {
  components: { Update },
  data() {
    return {
      isLoading: false,
      isSubmitting: false,
      newsFeed: null,
      form: {
        publisher: null,
        url: null,
      },
    };
  },
  mounted() {
    this.isLoading = false;
    this.newsFeed = null;
    this.loadData();
  },
  methods: {
    loadData() {
      axios
        .get(`/api/news-feeds/${this.$route.params.id}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.newsFeed = response.data;
          this.form = this.newsFeed;
        });
    },
    deleteItem() {
      if (confirm(this.$t("app.admin.newsFeeds.deleteConfirmation"))) {
        axios.delete(`/api/news-feeds/${this.$route.params.id}`).then(() => {
          this.$root.makeSuccessToast(
            this.$t("app.admin.newsFeeds.deletedMessage")
          );
          this.$root.goBack(`/admin/user-feeds`);
        });
      }
    },
  },
};
</script>
