<template>
  <div>
    <ValidatedInput
      :label="$t('app.admin.newsFeeds.publisher')"
      name="publisher"
      v-model="innerModel.publisher"
      rules="required|max:255"
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
import FormPartMixin from "@/mixins/FormPartMixin.js";
import ValidatedInput from "@/components/ValidatedInput.vue";
export default {
  mixins: [FormPartMixin],
  components: { ValidatedInput },
};
</script>
