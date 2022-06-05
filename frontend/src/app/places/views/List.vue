<template>
  <DefaultPage :title="$t('app.places.list.title')">
    <DefaultList url="/api/places">
      <template #item="{ item }">
        <div class="p-2">
          {{ item.name }}
          <b-link :to="`/places/${item.id}`" class="stretched-link"></b-link>
        </div>
      </template>
    </DefaultList>
  </DefaultPage>
</template>

<script>
import httpService from "@/services/http.service";
export default {
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

      this.$router.push({ path: `places/${items[0].id}` });
    },
  },
};
</script>
