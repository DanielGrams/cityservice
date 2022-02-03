<template>
  <div>
    <ValidationProvider
      :vid="vid"
      :name="$attrs.label"
      :rules="rules"
      v-slot="validationContext"
    >
      <b-form-group v-bind="$attrs">
        <b-form-input
          v-model="innerValue"
          v-bind="$attrs"
          :id="$attrs.name"
          :state="getValidationState(validationContext)"
        ></b-form-input>
        <b-form-invalid-feedback
          :state="getValidationState(validationContext)"
          :id="$attrs.name + '-error'"
        >
          {{ validationContext.errors[0] }}
        </b-form-invalid-feedback>
      </b-form-group>
    </ValidationProvider>
  </div>
</template>
<script>
export default {
  name: "ValidatedInput",
  props: {
    vid: {
      type: String,
    },
    rules: {
      type: [Object, String],
      default: "",
    },
    value: {
      type: null,
    },
  },
  data: () => ({
    innerValue: "",
  }),
  watch: {
    // Handles internal model changes.
    innerValue(newVal) {
      this.$emit("input", newVal);
    },
    // Handles external model changes.
    value(newVal) {
      this.innerValue = newVal;
    },
  },
  created() {
    /* istanbul ignore next */
    if (this.value) {
      this.innerValue = this.value;
    }
  },
  methods: {
    getValidationState({ dirty, validated, valid = null }) {
      return dirty || validated ? valid : null;
    },
  },
};
</script>
