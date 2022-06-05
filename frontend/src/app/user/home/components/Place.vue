<template>
  <div class="mb-4">
    <div class="section-title">{{ place.name }}</div>
    <WeatherWarningList :place="place" class="mb-2" />
    <NewsList :place="place" class="mb-2" />
  </div>
</template>

<script>
import NewsList from "./NewsList.vue";
import WeatherWarningList from "./WeatherWarningList.vue";

export default {
  components: { NewsList, WeatherWarningList },
  props: {
    place: {
      type: Object,
    },
  },
};
</script>
