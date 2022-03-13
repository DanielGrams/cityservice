<template>
  <div>
    <ValidatedInput
      :label="$t('app.admin.places.recyclingIds')"
      name="recycling_ids"
      v-model="innerModel.recycling_ids"
      rules="max:255"
    />
    <ValidatedInput
      :label="$t('app.admin.places.weatherWarningName')"
      name="weather_warning_name"
      v-model="innerModel.weather_warning_name"
      rules="max:255"
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
