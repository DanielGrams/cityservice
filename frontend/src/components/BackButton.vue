<template>
  <b-button variant="light" class="mb-2 mr-2" @click="goBack">
    <b-icon icon="chevron-left"></b-icon>
  </b-button>
</template>
<script>
export default {
  name: "BackButton",
  props: {
    path: {
      type: String,
    },
  },
  methods: {
    /* istanbul ignore next */
    goBack() {
      this.$root.goBack(this.path);
    },
  },
};
</script>
