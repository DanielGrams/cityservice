<template>
  <div>
    <h4>{{ place.name }}</h4>
    <WeatherWarningList :place="place" />
    <NewsList :place="place" />
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
