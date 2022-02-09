<template>
  <div>
    <ValidatedInput
      :label="$t('app.admin.newsFeeds.publisher')"
      name="publisher"
      v-model="innerModel.publisher"
      rules="required"
    />
    <ValidatedInput
      :label="$t('app.admin.newsFeeds.url')"
      name="url"
      v-model="innerModel.url"
      rules="required|url"
    />
  </div>
</template>

<script>
import ValidatedInput from "@/components/ValidatedInput.vue";
export default {
  components: { ValidatedInput },
  props: {
    model: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      innerModel: {},
    };
  },
  created() {
    this.innerModel = this.model;
  },
};
</script>
