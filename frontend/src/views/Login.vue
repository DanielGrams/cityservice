<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-form @submit.stop.prevent="handleSubmit(submitForm)">
        <ValidatedInput
          :label="$t('login.email')"
          name="email"
          v-model="email"
          rules="required|email"
        />
        <ValidatedInput
          :label="$t('login.password')"
          name="password"
          type="password"
          v-model="password"
          rules="required"
        />
        <b-button
          variant="primary"
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
import ValidatedInput from "@/components/common/ValidatedInput.vue";
export default {
  name: "Login",
  components: { ValidatedInput },
  data() {
    return {
      email: "",
      password: "",
      isSubmitting: false,
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.replace({ name: "Profile" });
    }
  },
  methods: {
    submitForm() {
      this.isSubmitting = true;

      this.$store
        .dispatch("auth/login", { email: this.email, password: this.password })
        .then(
          () => {
            if (this.$route.query.redirectTo) {
              this.$router.replace(this.$route.query.redirectTo);
            } else {
              this.$router.replace({ name: "Profile" });
            }
          },
          () => {
            this.isSubmitting = false;
            this.$root.makeErrorToast(this.$t("login.errorMessage"));
          }
        );
    },
  },
};
</script>
