<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-modal
        ref="modal"
        scrollable
        :title="title"
        @shown="modalShown"
        @ok.prevent="handleSubmit(submitForm)"
      >
        <b-form>
          <slot v-bind:formData="internalFormData"></slot>
        </b-form>
        <template #modal-footer="{ ok, cancel }">
          <b-button
            variant="secondary"
            @click="cancel()"
            :disabled="isSubmitting"
            >{{ $t("shared.cancel") }}</b-button
          >
          <b-button
            variant="primary"
            @click="ok()"
            :disabled="isSubmitting"
            class="submit-create-modal-btn"
          >
            <b-spinner small v-if="isSubmitting"></b-spinner>
            {{ $t("shared.submit") }}
          </b-button>
        </template>
      </b-modal>
    </ValidationObserver>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";

export default {
  props: {
    title: {
      type: String,
    },
    successMessage: {
      type: String,
    },
    url: {
      type: String,
    },
    formData: {
      type: Object,
    },
  },
  data() {
    return {
      isSubmitting: false,
      internalFormData: Vue.util.extend({}, this.formData),
    };
  },
  methods: {
    modalShown() {
      Object.keys(this.formData).forEach((key) => {
        if (Object.prototype.hasOwnProperty.call(this.internalFormData, key)) {
          this.internalFormData[key] = this.formData[key];
        }
      });
    },
    submitForm() {
      axios
        .post(this.url, this.internalFormData, {
          handleLoading: (isLoading) => (this.isSubmitting = isLoading),
        })
        .then(() => {
          this.$root.makeSuccessToast(this.successMessage);
          this.hideModal();
          this.$emit("created", this.internalFormData);
        });
    },
    showModal() {
      this.$refs["modal"].show();
    },
    hideModal() {
      this.$refs["modal"].hide();
    },
  },
};
</script>
