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
        <b-table stacked :fields="propertyFields" :items="properties">
        </b-table>
      </div>
    </b-overlay>
  </div>
</template>

<script>
import httpService from "@/services/http.service";
import Update from "../components/Update.vue";
import { localizeFeedType } from "../common.js";

export default {
  components: { Update },
  computed: {
    properties() {
      return [this.newsFeed];
    },
  },
  data() {
    return {
      isLoading: false,
      newsFeed: null,
      propertyFields: [
        {
          key: "url",
          label: this.$t("app.admin.newsFeeds.url"),
        },
        {
          key: "feed_type",
          label: this.$t("app.admin.newsFeeds.feedType"),
          formatter: (value) => {
            return localizeFeedType(value);
          },
        },
        {
          key: "place.name",
          label: this.$t("app.admin.newsFeeds.place"),
        },
        {
          key: "title_filter",
          label: this.$t("app.admin.newsFeeds.titleFilter"),
        },
        {
          key: "title_sub_pattern",
          label: this.$t("app.admin.newsFeeds.titleSubPattern"),
        },
        {
          key: "title_sub_repl",
          label: this.$t("app.admin.newsFeeds.titleSubRepl"),
        },
      ],
    };
  },
  mounted() {
    this.isLoading = false;
    this.newsFeed = null;
    this.loadData();
  },
  methods: {
    loadData() {
      httpService
        .get(`/api/news-feeds/${this.$route.params.id}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.newsFeed = response.data;
        });
    },
    deleteItem() {
      if (confirm(this.$t("app.admin.newsFeeds.deleteConfirmation"))) {
        httpService
          .delete(`/api/news-feeds/${this.$route.params.id}`)
          .then(() => {
            this.$root.makeSuccessToast(
              this.$t("app.admin.newsFeeds.deletedMessage")
            );
            this.$root.goBack(`/admin/news-feeds`);
          });
      }
    },
  },
};
</script>
