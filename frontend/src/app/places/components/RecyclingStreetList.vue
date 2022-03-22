<template>
  <div class="p-3">
    <b-form-input
      id="filter-input"
      v-model="filter"
      type="search"
      :placeholder="$t('shared.filter.instruction')"
      class="mb-2"
    ></b-form-input>
    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>
    <b-table
      ref="table"
      id="select-recycling-street-table"
      :fields="fields"
      :items="loadTableData"
      :current-page="currentPage"
      :per-page="perPage"
      :filter="filter"
      filter-debounce="500"
      primary-key="id"
      thead-class="d-none"
      outlined
      hover
      responsive
      show-empty
      :empty-text="$t('shared.emptyData')"
      style="min-height: 120px"
      selectable
      @row-selected="onRowSelected"
    >
    </b-table>
    <b-pagination
      v-if="totalRows > perPage"
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      aria-controls="select-recycling-street-table"
    ></b-pagination>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      filter: "",
      errorMessage: null,
      fields: [
        {
          key: "name",
          tdClass: "align-middle",
        },
      ],
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
      let params = {
        page: ctx.currentPage,
        per_page: ctx.perPage,
      };

      if (ctx.filter != null && ctx.filter != "") {
        params["keyword"] = ctx.filter;
      }

      const vm = this;
      axios
        .get(`/api/places/${this.$route.params.id}/recycling-streets`, {
          params: params,
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
    onRowSelected(items) {
      /* istanbul ignore next */
      if (items.length < 1) {
        return;
      }

      this.$router.push({ path: `/recycling-streets/${items[0].id}` });
    },
  },
};
</script>
