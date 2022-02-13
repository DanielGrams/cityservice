<template>
  <div>
    <UpdateModalForm
      ref="form"
      v-on="$listeners"
      :id="id"
      :formData="form"
      :title="$t('app.admin.newsFeeds.update.title')"
      :successMessage="$t('app.admin.newsFeeds.update.successMessage')"
      url="/api/news-feeds"
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
        publisher: null,
        url: null,
        title_filter: null,
        title_sub_pattern: null,
        title_sub_repl: null,
      },
    };
  },
};
</script>
