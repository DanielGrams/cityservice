<template>
  <DefaultPage :title="$t('app.user.places.title')">
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
        responsive
        show-empty
        :empty-text="$t('shared.emptyData')"
        style="min-height: 120px"
      >
        <template #cell(actions)="data">
          <b-button
            @click="togglePlace(data.item)"
            class="favorite-btn"
            variant="light"
            ><b-icon
              :icon="data.item.is_favored ? 'star-fill' : 'star'"
            ></b-icon
          ></b-button>
        </template>
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
    togglePlace(place) {
      if (place.is_favored) {
        httpService.delete(`/api/user/places/${place.id}`).then(() => {
          place.is_favored = false;
        });
      } else {
        httpService.put(`/api/user/places/${place.id}`).then(() => {
          place.is_favored = true;
        });
      }
    },
  },
};
</script>
