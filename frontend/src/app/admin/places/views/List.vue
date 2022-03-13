<template>
  <div>
    <h3>{{ $t("app.admin.places.list.title") }}</h3>

    <b-button-group class="my-4">
      <b-button
        @click="$refs.create.showModal()"
        variant="light"
        class="add-btn"
        ><b-icon icon="plus"></b-icon
      ></b-button>
    </b-button-group>

    <Create ref="create" @created="refreshTableData" />

    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>

    <b-table
      ref="table"
      id="main-table"
      :fields="fields"
      :items="loadTableData"
      :current-page="currentPage"
      :per-page="perPage"
      primary-key="id"
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
      aria-controls="main-table"
    ></b-pagination>
  </div>
</template>

<script>
import axios from "axios";
import Create from "../components/Create.vue";
export default {
  components: { Create },
  data() {
    return {
      errorMessage: null,
      fields: [
        {
          key: "name",
          label: this.$t("app.admin.places.name"),
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
      const vm = this;
      axios
        .get(`/api/places`, {
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
    refreshTableData() {
      this.$refs.table.refresh();
    },
    onRowSelected(items) {
      /* istanbul ignore next */
      if (items.length < 1) {
        return;
      }

      this.$router.push({ path: `places/${items[0].id}` });
    },
  },
};
</script>
