<template>
  <NewsList />
</template>

<script>
import NewsList from "@/components/NewsList.vue";

export default {
  name: "News",
  metaInfo: {
    title: "News",
  },
  components: {
    NewsList,
  },
};
</script>
