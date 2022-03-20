<template>
  <div class="p-3">
    <b-list-group>
      <b-list-group-item
        v-for="item in items"
        :key="item.id"
        :href="item.link_url"
        target="_blank"
      >
        <div class="d-flex flex-row align-items-center">
          <div class="m-3" style="max-width: 40px">
            <img
              :src="item.publisher_icon_url"
              class="img-fluid rounded"
              style="max-width: 40px"
            />
          </div>
          <div class="">
            <small>{{ item.published | moment("dd. DD.MM.YYYY") }}</small>
            <h5 class="mb-1">{{ item.news_feed.publisher }}</h5>
            <p class="mb-1">{{ item.content }}</p>
          </div>
        </div>
      </b-list-group-item>
    </b-list-group>
    <b-pagination
      v-if="totalRows > perPage"
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      class="mt-4"
    ></b-pagination>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      totalRows: 0,
      currentPage: 1,
      perPage: 10,
      items: [],
    };
  },
  watch: {
    currentPage() {
      this.refreshData();
    },
  },
  created() {
    this.refreshData();
  },
  methods: {
    refreshData() {
      axios
        .get(`/api/places/${this.$route.params.id}/news-items`, {
          params: {
            page: this.currentPage,
            per_page: this.perPage,
          },
        })
        .then((response) => {
          this.totalRows = response.data.total;
          this.items = response.data.items;
        });
    },
  },
};
</script>
