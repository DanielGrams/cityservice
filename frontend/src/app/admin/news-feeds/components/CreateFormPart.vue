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
    <ValidatedSelect
      :label="$t('app.admin.newsFeeds.feedType')"
      name="feed_type"
      v-model="innerModel.feed_type"
      :options="feedOptions"
      rules="required"
    />
  </div>
</template>

<script>
import FormPartMixin from "@/mixins/FormPartMixin.js";
import ValidatedInput from "@/components/ValidatedInput.vue";
import ValidatedSelect from "@/components/ValidatedSelect.vue";
import { getLocalizedFeedTypes } from "../common.js";
export default {
  mixins: [FormPartMixin],
  components: { ValidatedInput, ValidatedSelect },
  data() {
    return {
      feedOptions: [],
    };
  },
  mounted() {
    this.feedOptions = getLocalizedFeedTypes();
  },
};
</script>
