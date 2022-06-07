<template>
  <div class="section my-4">
    <div class="section-title" v-if="show">
      {{ $t("app.home.recyclingEvents") }}
    </div>
    <DefaultList
      url="/api/user/recycling-events"
      :showEmpty="false"
      @isEmptyChanged="(value) => (show = !value)"
      ref="list"
    >
      <template #item="data">
        <div class="d-flex flex-row align-items-center px-3 py-2">
          <div>
            <div class="list-item-title">
              {{ data.item.category }}
            </div>
            <div class="list-item-detail">
              {{ data.item.street.name }}
            </div>

            <div class="list-item-head">
              {{ data.item.date | moment("dd. DD.MM.YYYY") }}
            </div>
          </div>
          <div class="ml-auto" style="max-width: 30px">
            <img
              :src="data.item.category_icon_url"
              class="img-fluid rounded"
              style="max-width: 30px; border-radius: 15px !important"
            />
          </div>
        </div>
      </template>
    </DefaultList>
  </div>
</template>

<script>
import DefaultList from "@/components/DefaultList";
export default {
  components: {
    DefaultList,
  },
  data() {
    return {
      show: true,
    };
  },
  methods: {
    refreshData() {
      this.$refs["list"].refreshData();
    },
  },
};
</script>
