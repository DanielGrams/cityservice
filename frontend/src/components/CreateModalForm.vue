<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-modal
        ref="modal"
        scrollable
        :title="title"
        @ok.prevent="handleSubmit(submitForm)"
      >
        <b-form>
          <slot v-bind:formData="formData"></slot>
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
    };
  },
  methods: {
    submitForm() {
      axios
        .post(this.url, this.formData, {
          handleLoading: (isLoading) => (this.isSubmitting = isLoading),
        })
        .then(() => {
          this.$root.makeSuccessToast(this.successMessage);
          this.hideModal();
          this.$emit("created", this.formData);
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
