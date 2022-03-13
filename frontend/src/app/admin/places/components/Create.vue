<template>
  <div>
    <CreateModalForm
      ref="form"
      v-on="$listeners"
      :formData="form"
      :title="$t('app.admin.places.create.title')"
      :successMessage="$t('app.admin.places.create.successMessage')"
      url="/api/places"
      #default="{ formData }"
    >
      <CreateFormPart :model="formData"></CreateFormPart>
    </CreateModalForm>
  </div>
</template>

<script>
import ModalFormMixin from "@/mixins/ModalFormMixin.js";
import CreateModalForm from "@/components/CreateModalForm.vue";
import CreateFormPart from "./CreateFormPart.vue";
export default {
  mixins: [ModalFormMixin],
  components: { CreateFormPart, CreateModalForm },
  data() {
    return {
      form: {
        name: null,
      },
    };
  },
};
</script>
