<template>
  <div class="mb-4">
    <h4 v-if="show">{{ $t("app.home.recyclingEvents") }}</h4>
    <DefaultList
      url="/api/user/recycling-events"
      :showEmpty="false"
      @isEmptyChanged="(value) => (show = !value)"
    >
      <template #item="data">
        <div class="d-flex flex-row align-items-center p-2">
          <div class="mx-3" style="max-width: 30px">
            <img
              :src="data.item.category_icon_url"
              class="img-fluid rounded"
              style="max-width: 30px; border-radius: 15px !important"
            />
          </div>
          <div>
            <div class="list-item-head">
              {{ data.item.date | moment("dd. DD.MM.YYYY") }}
              {{ data.item.place.name }}
            </div>
            <div class="list-item-title">
              {{ data.item.street.name }}: {{ data.item.category }}
            </div>
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
};
</script>
