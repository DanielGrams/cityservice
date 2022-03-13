<template>
  <div>
    <ValidatedInput
      :label="$t('app.admin.places.name')"
      name="name"
      v-model="innerModel.name"
      rules="required|max:255"
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
