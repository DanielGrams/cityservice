<template>
  <div class="">
    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>
    <div class="alert alert-light" role="alert" v-if="showEmpty && isEmpty">
      {{ $t("shared.emptyData") }}
    </div>
    <b-overlay :show="isLoading">
      <b-list-group>
        <b-list-group-item v-for="item in items" :key="item.id" class="p-0">
          <slot name="item" :item="item"></slot>
        </b-list-group-item>
        <slot name="footer"></slot>
      </b-list-group>
      <b-pagination
        v-if="showPagination && totalRows > perPage"
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="internalPerPage"
        class="mt-2"
      ></b-pagination>
    </b-overlay>
  </div>
</template>
<script>
import httpService from "@/services/http.service";
import RefreshableMixin from "@/mixins/RefreshableMixin";

export default {
  name: "DefaultList",
  mixins: [RefreshableMixin],
  props: {
    url: {
      type: String,
    },
    perPage: {
      type: Number,
      default: 10,
    },
    showEmpty: {
      type: Boolean,
      default: true,
    },
    showPagination: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      isLoading: false,
      errorMessage: null,
      totalRows: 0,
      currentPage: 1,
      internalPerPage: 10,
      items: [],
    };
  },
  computed: {
    isEmpty() {
      return !this.isLoading && !this.errorMessage && this.totalRows == 0;
    },
  },
  watch: {
    isEmpty(value) {
      this.$emit("isEmptyChanged", value);
    },
    /* istanbul ignore next */
    currentPage() /* istanbul ignore next */ {
      this.refreshData();
    },
  },
  created() {
    this.internalPerPage = this.perPage;
  },
  mounted() {
    this.refreshData();
  },
  methods: {
    async refreshData() {
      this.onRefreshingDataStarted();
      const response = await httpService.get(this.url, {
        params: {
          page: this.currentPage,
          per_page: this.internalPerPage,
        },
        handleLoading: (isLoading) => (this.isLoading = isLoading),
        handleRequestStart: () => (this.errorMessage = null),
        handleRequestError: /* istanbul ignore next */ (
          _error,
          message
        ) => /* istanbul ignore next */ {
          this.errorMessage = message;
        },
      });

      this.totalRows = response.data.total;
      this.items = response.data.items;
    },
  },
};
</script>
