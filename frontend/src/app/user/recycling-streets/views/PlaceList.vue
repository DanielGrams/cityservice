<template>
  <DefaultPage :title="$t('app.user.recyclingStreets.places.title')">
    <template #left>
      <BackButton path="/user/profile" />
    </template>
    <div>
      <div class="alert alert-danger" role="alert" v-if="errorMessage">
        {{ errorMessage }}
      </div>
      <b-table
        ref="table"
        id="select-place-table"
        :fields="fields"
        :items="loadTableData"
        :current-page="currentPage"
        :per-page="perPage"
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
        aria-controls="select-place-table"
      ></b-pagination>
    </div>
  </DefaultPage>
</template>

<script>
import httpService from "@/services/http.service";
import BackButton from "@/components/BackButton.vue";
export default {
  components: {
    BackButton,
  },
  data() {
    return {
      errorMessage: null,
      fields: [
        {
          key: "name",
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
      httpService
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
    onRowSelected(items) {
      /* istanbul ignore next */
      if (items.length < 1) {
        return;
      }

      this.$router.push({ path: `places/${items[0].id}/recycling-streets` });
    },
  },
};
</script>
