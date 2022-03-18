<template>
  <b-overlay :show="isLoading">
    <div>
      <h4 class="d-flex justify-content-between align-items-center">
        <span>{{ $t("app.user.profile.recyclingStreets.title") }}</span>
        <b-button-group style="padding-right: 0.75rem">
          <b-button
            to="/user/recycling-streets/places"
            variant="secondary"
            id="add-recycling-street-btn"
            ><b-icon icon="plus"></b-icon
          ></b-button>
        </b-button-group>
      </h4>

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
        responsive
        thead-class="d-none"
        show-empty
        :empty-text="$t('shared.emptyData')"
        style="min-height: 120px"
      >
        <template #cell(actions)="data">
          <b-button
            @click="deleteRecyclingStreet(data.item)"
            class="remove-recycling-street-btn"
            variant="light"
            ><b-icon icon="x"></b-icon
          ></b-button>
        </template>
      </b-table>
      <b-pagination
        v-if="totalRows > perPage"
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="perPage"
        aria-controls="main-table"
      ></b-pagination>
    </div>
  </b-overlay>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      errorMessage: null,
      fields: [
        {
          key: "name",
          tdClass: "align-middle",
        },
        {
          key: "actions",
          tdClass: "text-right align-middle",
        },
      ],
      totalRows: 0,
      currentPage: 1,
      perPage: 10,
      searchResult: {
        items: [],
      },
      isLoading: false,
    };
  },
  methods: {
    loadTableData(ctx, callback) {
      const vm = this;
      axios
        .get(`/api/user/recycling-streets`, {
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
    deleteRecyclingStreet(recyclingStreet) {
      if (
        confirm(this.$t("app.user.profile.recyclingStreets.deleteConfirmation"))
      ) {
        axios
          .delete(`/api/user/recycling-streets/${recyclingStreet.id}`)
          .then(() => {
            this.$root.makeSuccessToast(
              this.$t("app.user.profile.recyclingStreets.deletedMessage")
            );
            this.refreshTableData();
          });
      }
    },
  },
};
</script>
