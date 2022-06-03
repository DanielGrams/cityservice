<template>
  <div class="">
    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>
    <b-table
      ref="table"
      id="select-weather-warning-table"
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
    >
      <template #cell(content)="data">
        <div class="weather-warning">
          <small
            >{{ data.item.start | moment("dd. DD.MM.YYYY HH:mm") }} Uhr -
            {{ data.item.end | moment("dd. DD.MM.YYYY HH:mm") }} Uhr</small
          >
          <h5 class="mb-1">{{ data.item.headline }}</h5>
          <div>{{ data.item.content }}</div>
        </div>
      </template>
    </b-table>
    <b-pagination
      v-if="totalRows > perPage"
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      aria-controls="select-weather-warning-table"
    ></b-pagination>
  </div>
</template>

<script>
import httpService from "@/services/http.service";
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
      perPage: 10,
      searchResult: {
        items: [],
      },
    };
  },
  methods: {
    loadTableData(ctx, callback) {
      const vm = this;
      httpService
        .get(`/api/places/${this.place.id}/weather-warnings`, {
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
  },
};
</script>
