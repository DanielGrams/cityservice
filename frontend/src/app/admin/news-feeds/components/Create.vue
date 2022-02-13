<template>
  <div>
    <CreateModalForm
      ref="form"
      v-on="$listeners"
      :formData="form"
      :title="$t('app.admin.newsFeeds.create.title')"
      :successMessage="$t('app.admin.newsFeeds.create.successMessage')"
      url="/api/news-feeds"
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
        publisher: null,
        url: null,
      },
    };
  },
};
</script>
