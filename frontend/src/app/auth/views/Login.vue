<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-form @submit.stop.prevent="handleSubmit(submitForm)">
        <ValidatedInput
          :label="$t('app.auth.login.email')"
          name="email"
          type="email"
          v-model="email"
          rules="required|email"
        />
        <ValidatedInput
          :label="$t('app.auth.login.password')"
          name="password"
          type="password"
          v-model="password"
          rules="required"
        />
        <b-button
          variant="primary"
          id="submit"
          type="submit"
          v-bind:disabled="isSubmitting"
        >
          <b-spinner small v-if="isSubmitting"></b-spinner>
          {{ $t("shared.submit") }}
        </b-button>
      </b-form>
    </ValidationObserver>
  </div>
</template>

<script>
import ValidatedInput from "@/components/ValidatedInput.vue";
export default {
  components: { ValidatedInput },
  data() {
    return {
      email: "",
      password: "",
      isSubmitting: false,
    };
  },
  methods: {
    submitForm() {
      this.isSubmitting = true;

      this.$store
        .dispatch("auth/login", { email: this.email, password: this.password })
        .then(
          () => {
            this.redirect();
          },
          () => {
            this.isSubmitting = false;
            this.$root.makeErrorToast(this.$t("app.auth.login.errorMessage"));
          }
        );
    },
    redirect() {
      if (this.$route.query.redirectTo) {
        this.$router.replace(this.$route.query.redirectTo);
      } else {
        this.$router.replace("/user/home");
      }
    },
  },
};
</script>
