<template>
  <div>
    <ValidatedTypeahead
      :labelValue="$t('app.admin.newsFeeds.place')"
      name="place"
      v-model="innerModel.place"
      fetchURL="/api/places?keyword={query}"
      :serializer="(i) => i.name"
      rules=""
    />
    <ValidatedInput
      :label="$t('app.admin.newsFeeds.titleFilter')"
      :description="$t('app.admin.newsFeeds.titleFilterDescription')"
      name="title_filter"
      v-model="innerModel.title_filter"
      rules="max:255"
    />
    <ValidatedInput
      :label="$t('app.admin.newsFeeds.titleSubPattern')"
      :description="$t('app.admin.newsFeeds.titleSubPatternDescription')"
      name="title_sub_pattern"
      v-model="innerModel.title_sub_pattern"
      rules="max:255"
    />
    <ValidatedInput
      :label="$t('app.admin.newsFeeds.titleSubRepl')"
      :description="$t('app.admin.newsFeeds.titleSubReplDescription')"
      name="title_sub_repl"
      v-model="innerModel.title_sub_repl"
      rules="max:255"
    />
  </div>
</template>

<script>
import FormPartMixin from "@/mixins/FormPartMixin.js";
import ValidatedInput from "@/components/ValidatedInput.vue";
import ValidatedTypeahead from "@/components/ValidatedTypeahead.vue";
export default {
  mixins: [FormPartMixin],
  components: { ValidatedInput, ValidatedTypeahead },
};
</script>
