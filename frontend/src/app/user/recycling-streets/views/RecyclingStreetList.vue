<template>
  <div class="container">
    <h3 class="d-flex justify-content-between align-items-center">
      <div>
        <BackButton path="/places" />
        <span>{{
          $t("app.user.recyclingStreets.recyclingStreets.title")
        }}</span>
      </div>
    </h3>
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
      responsive
      show-empty
      :empty-text="$t('shared.emptyData')"
      style="min-height: 120px"
    >
      <template #cell(actions)="data">
        <b-button
          @click="toggleStreet(data.item)"
          class="favorite-btn"
          variant="light"
          ><b-icon :icon="data.item.is_favored ? 'star-fill' : 'star'"></b-icon
        ></b-button>
      </template>
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
import httpService from "@/services/http.service";
import BackButton from "@/components/BackButton.vue";
export default {
  components: {
    BackButton,
  },
  data() {
    return {
      filter: "",
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
      httpService
        .get(`/api/places/${this.$route.params.placeId}/recycling-streets`, {
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
    toggleStreet(street) {
      if (street.is_favored) {
        httpService
          .delete(`/api/user/recycling-streets/${street.id}`)
          .then(() => {
            street.is_favored = false;
          });
      } else {
        httpService.put(`/api/user/recycling-streets/${street.id}`).then(() => {
          street.is_favored = true;
        });
      }
    },
  },
};
</script>
