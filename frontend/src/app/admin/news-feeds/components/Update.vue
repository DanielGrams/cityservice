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
      <Form :model="formData"></Form>
    </UpdateModalForm>
  </div>
</template>

<script>
import UpdateModalForm from "@/components/UpdateModalForm.vue";
import Form from "./Form.vue";
export default {
  components: { Form, UpdateModalForm },
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
