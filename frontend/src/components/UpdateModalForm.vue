<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-modal
        ref="modal"
        @show="loadData"
        :title="title"
        @ok.prevent="handleSubmit(submitForm)"
      >
        <b-form>
          <b-overlay :show="isLoading">
            <slot v-bind:formData="formData"></slot>
          </b-overlay>
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
            class="submit-update-modal-btn"
            @click="ok()"
            :disabled="isSubmitting || isLoading"
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
    id: {
      type: String,
    },
    formData: {
      type: Object,
    },
  },
  data() {
    return {
      isSubmitting: false,
      isLoading: false,
      instance: null,
    };
  },
  methods: {
    loadData() {
      /* istanbul ignore next */
      if (this.id == null) {
        return;
      }

      axios
        .get(`${this.url}/${this.id}`, {
          handleLoading: (isLoading) => (this.isLoading = isLoading),
        })
        .then((response) => {
          this.instance = response.data;

          Object.keys(response.data).forEach((key) => {
            if (Object.prototype.hasOwnProperty.call(this.formData, key)) {
              this.formData[key] = response.data[key];
            }
          });
        });
    },
    submitForm() {
      axios
        .put(`${this.url}/${this.id}`, this.formData, {
          handleLoading: (isLoading) => (this.isSubmitting = isLoading),
        })
        .then(() => {
          this.$root.makeSuccessToast(this.successMessage);
          this.hideModal();
          this.$emit("updated", this.formData);
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
