<template>
  <div>
    <validation-provider
      :name="label"
      :detectInput="false"
      ref="validationProvider"
      :rules="rules"
      v-slot="validationContext"
    >
      <b-form-group :label="label" :id="$attrs.name">
        <VueTypeaheadBootstrap
          ref="typeahead"
          v-model="query"
          :data="suggestions"
          :minMatchingChars="1"
          :disableSort="true"
          :showAllResults="true"
          :placeholder="
            $attrs.placeholder != null
              ? $attrs.placeholder
              : $t('shared.typeahead.instruction')
          "
          :inputClass="getInputClass(validationContext)"
          @hit="selected = $event"
          @input="onInput"
          v-bind="$attrs"
        />
        <b-form-invalid-feedback
          :state="getValidationState(validationContext)"
          :id="$attrs.name + '-error'"
        >
          {{ validationContext.errors[0] }}
        </b-form-invalid-feedback>
      </b-form-group>
    </validation-provider>
  </div>
</template>
<script>
import axios from "axios";
import _debounce from "lodash/debounce";
import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";

export default {
  components: { VueTypeaheadBootstrap },
  props: {
    value: {
      type: null,
    },
    rules: {
      type: [Object, String],
      default: "required",
    },
    fetchURL: {
      type: String,
    },
    labelKey: {
      type: String,
    },
    labelValue: {
      type: String,
    },
    validClass: {
      type: String,
      default: "is-valid",
    },
    invalidClass: {
      type: String,
      default: "is-invalid",
    },
  },
  data: () => ({
    query: "",
    suggestions: [],
    selected: null,
  }),
  computed: {
    label() {
      return this.labelValue != null ? this.labelValue : this.$t(this.labelKey);
    },
  },
  watch: {
    // Handles internal model changes.
    selected(newVal) {
      this.$emit("input", newVal);
      this.$refs.validationProvider.syncValue(newVal);
      this.$refs.validationProvider.validate();
    },
    // Handles external model changes.
    value(newVal) {
      this.selected = newVal;
      this.$refs.typeahead.inputValue =
        newVal != null ? this.$refs.typeahead.serializer(newVal) : null;
    },
  },
  methods: {
    getValidationState({ dirty, validated, valid = null }) {
      return dirty || validated ? valid : null;
    },
    getInputClass({ dirty, validated, valid = null }) {
      if (dirty || !validated) {
        return "";
      }

      return valid ? this.validClass : this.invalidClass;
    },
    fetchData(query) {
      const vm = this;
      axios.get(this.fetchURL.replace("{query}", query)).then((response) => {
        vm.suggestions = response.data.items;
      });
    },
    fetchDataDebounced: _debounce(function (query) {
      this.fetchData(query);
    }, 500),
    onInput() {
      this.selected = null;
      this.fetchDataDebounced(this.query);
    },
  },
  mounted() {
    this.$refs.validationProvider.syncValue(this.selected);

    this.$watch("$refs.typeahead.isFocused", (new_value) => {
      /* istanbul ignore next */
      if (new_value && this.$refs.typeahead.showOnFocus && this.query == "") {
        this.fetchData(this.query);
      }
    });
  },
};
</script>
