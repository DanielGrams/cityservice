<template>
  <div class="">
    <DefaultList :url="url" :showEmpty="false">
      <template #item="data">
        <div class="weather-warning px-3 py-2">
          <div class="list-item-title">{{ data.item.headline }}</div>
          <div class="list-item-detail">{{ data.item.content }}</div>
          <div class="list-item-head">
            {{ data.item.start | moment("dd. DD.MM.YYYY HH:mm") }} Uhr -
            {{ data.item.end | moment("dd. DD.MM.YYYY HH:mm") }} Uhr
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
  props: {
    place: {
      type: Object,
    },
  },
  computed: {
    url() {
      return `/api/places/${this.place.id}/weather-warnings`;
    },
  },
};
</script>
