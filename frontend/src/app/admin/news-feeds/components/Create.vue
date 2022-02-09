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
      <Form :model="formData"></Form>
    </CreateModalForm>
  </div>
</template>

<script>
import CreateModalForm from "@/components/CreateModalForm.vue";
import Form from "./Form.vue";
export default {
  components: { Form, CreateModalForm },
  data() {
    return {
      form: {
        publisher: null,
        url: null,
      },
    };
  },
  methods: {
    showModal() {
      this.$refs["form"].showModal();
    },
  },
};
</script>
