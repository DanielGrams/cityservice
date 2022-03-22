<template>
  <div class="p-3">
    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>
    <b-table
      ref="table"
      id="recycling-events-table"
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
        <div class="d-flex flex-row align-items-center">
          <div class="m-2" style="max-width: 40px">
            <img
              :src="data.item.category_icon_url"
              class="img-fluid rounded"
              style="max-width: 40px"
            />
          </div>
          <div>
            <small>{{ data.item.date | moment("dd. DD.MM.YYYY") }}</small>
            <h5 class="mb-1">{{ data.item.category }}</h5>
          </div>
        </div>
      </template>
    </b-table>
    <b-pagination
      v-if="totalRows > perPage"
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      aria-controls="recycling-events-table"
    ></b-pagination>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      errorMessage: null,
      fields: ["content"],
      totalRows: 0,
      currentPage: 1,
      perPage: 10,
    };
  },
  methods: {
    loadTableData(ctx, callback) {
      const vm = this;
      axios
        .get(`/api/recycling-streets/${this.$route.params.id}/events`, {
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
