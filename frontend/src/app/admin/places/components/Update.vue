<template>
  <div>
    <UpdateModalForm
      ref="form"
      v-on="$listeners"
      :id="id"
      :formData="form"
      :title="$t('app.admin.places.update.title')"
      :successMessage="$t('app.admin.places.update.successMessage')"
      url="/api/places"
      #default="{ formData }"
    >
      <CreateFormPart :model="formData"></CreateFormPart>
      <UpdateFormPart :model="formData"></UpdateFormPart>
    </UpdateModalForm>
  </div>
</template>

<script>
import ModalFormMixin from "@/mixins/ModalFormMixin.js";
import UpdateModalForm from "@/components/UpdateModalForm.vue";
import CreateFormPart from "./CreateFormPart.vue";
import UpdateFormPart from "./UpdateFormPart.vue";
export default {
  mixins: [ModalFormMixin],
  components: { CreateFormPart, UpdateFormPart, UpdateModalForm },
  props: {
    id: {
      type: String,
    },
  },
  data() {
    return {
      form: {
        name: null,
        recycling_ids: null,
        weather_warning_name: null,
      },
    };
  },
};
</script>
