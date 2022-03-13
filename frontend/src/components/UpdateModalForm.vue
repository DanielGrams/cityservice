<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-modal
        ref="modal"
        scrollable
        :title="title"
        @show="modalShow"
        @ok.prevent="handleSubmit(submitForm)"
      >
        <b-form ref="formform">
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
import Vue from "vue";
import axios from "axios";
import _omit from "lodash/omit";

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
    removeFromSendData: {
      type: Array,
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
    modalShow() {
      this.loadData();
    },
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
      let putData = Vue.util.extend({}, this.formData);

      if (this.removeFromSendData != null) {
        putData = _omit(this.formData, this.removeFromSendData);
      }

      axios
        .put(`${this.url}/${this.id}`, putData, {
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
