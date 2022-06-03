<template>
  <div class="">
    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>
    <b-table
      ref="table"
      id="news-item-table"
      :fields="fields"
      :items="loadTableData"
      :current-page="currentPage"
      :per-page="perPage"
      primary-key="id"
      thead-class="d-none"
      outlined
      responsive
      show-empty
      :empty-text="$t('shared.emptyData')"
      style="min-height: 120px"
      class="mb-0"
    >
      <template #cell(content)="data">
        <div
          class="news-item d-flex flex-row align-items-center position-relative"
        >
          <div class="m-3" style="max-width: 40px">
            <img
              :src="data.item.publisher_icon_url"
              class="img-fluid rounded"
              style="max-width: 40px"
            />
          </div>
          <div>
            <small>{{ data.item.published | moment("dd. DD.MM.YYYY") }}</small>
            <h5 class="mb-1">{{ data.item.news_feed.publisher }}</h5>
            <p class="mb-1">{{ data.item.content }}</p>
          </div>
          <a
            href="#"
            @click.prevent="newsItemClicked(data.item)"
            class="stretched-link"
          ></a>
        </div>
      </template>
    </b-table>
    <b-button variant="link" :to="`/places/${this.place.id}`" class="mb-3">{{
      $t("app.home.news.more", { placeName: this.place.name })
    }}</b-button>
  </div>
</template>

<script>
import httpService from "@/services/http.service";
import { Browser } from "@capacitor/browser";
export default {
  props: {
    place: {
      type: Object,
    },
  },
  data() {
    return {
      errorMessage: null,
      fields: ["content"],
      totalRows: 0,
      currentPage: 1,
      perPage: 5,
      items: [],
    };
  },
  methods: {
    loadTableData(ctx, callback) {
      const vm = this;
      httpService
        .get(`/api/places/${this.place.id}/news-items`, {
          params: {
            page: ctx.currentPage,
            per_page: ctx.perPage,
          },
          handleRequestStart: () => (this.errorMessage = null),
          handleRequestError: /* istanbul ignore next */ (
            _error,
            message
          ) => /* istanbul ignore next */ {
            this.errorMessage = message;
            callback([]);
          },
        })
        .then((response) => {
          vm.totalRows = response.data.total;
          callback(response.data.items);
        });
      return null;
    },
    /* istanbul ignore next */
    newsItemClicked(item) {
      Browser.open({ url: item.link_url });
    },
  },
};
</script>
