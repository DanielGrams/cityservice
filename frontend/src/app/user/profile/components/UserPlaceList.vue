<template>
  <b-overlay :show="isLoading">
    <div>
      <h4 class="d-flex justify-content-between align-items-center">
        <span>{{ $t("app.user.profile.places.title") }}</span>
        <b-button-group style="padding-right: 0.75rem">
          <b-button to="/user/places" variant="secondary" id="add-place-btn"
            ><b-icon icon="plus"></b-icon
          ></b-button>
        </b-button-group>
      </h4>

      <div class="alert alert-danger" role="alert" v-if="errorMessage">
        {{ errorMessage }}
      </div>

      <b-table
        ref="table"
        id="user-place-table"
        :fields="fields"
        :items="loadTableData"
        :current-page="currentPage"
        :per-page="perPage"
        primary-key="id"
        outlined
        hover
        responsive
        thead-class="d-none"
        show-empty
        :empty-text="$t('shared.emptyData')"
        style="min-height: 120px"
        selectable
        @row-selected="onRowSelected"
      >
        <template #cell(actions)="data">
          <b-button
            @click="deletePlace(data.item)"
            class="remove-place-btn"
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
        aria-controls="user-place-table"
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
        .get(`/api/user/places`, {
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
    deletePlace(place) {
      if (confirm(this.$t("app.user.profile.places.deleteConfirmation"))) {
        axios.delete(`/api/user/places/${place.id}`).then(() => {
          this.$root.makeSuccessToast(
            this.$t("app.user.profile.places.deletedMessage")
          );
          this.refreshTableData();
        });
      }
    },
    onRowSelected(items) {
      /* istanbul ignore next */
      if (items.length < 1) {
        return;
      }

      this.$router.push({ path: `/places/${items[0].id}` });
    },
  },
};
</script>
