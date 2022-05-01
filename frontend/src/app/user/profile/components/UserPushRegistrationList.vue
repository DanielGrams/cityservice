<template>
  <div>
    <h4>{{ $t("app.user.profile.notifications.title") }}</h4>
    <div v-if="!notificationsSupported">
      {{ $t("app.notifications.notSupported") }}
    </div>
    <div v-if="notificationsSupported">
      <div v-if="notificationPermission == 'denied'">
        {{ $t("app.notifications.permissionDenied") }}
      </div>
      <div v-if="notificationPermission != 'denied'">
        <div v-if="!pushRegistrationId">
          <div>{{ $t("app.user.profile.notifications.notRegistered") }}</div>
          <b-button @click="registerPush" class="my-2">{{
            $t("app.user.profile.notifications.registerPush")
          }}</b-button>
        </div>
        <div v-if="pushRegistrationId">
          <div>{{ $t("app.user.profile.notifications.registered") }}</div>
          <b-button @click="unregisterPush" class="my-2 mr-2">{{
            $t("app.user.profile.notifications.unregisterPush")
          }}</b-button>
          <b-button @click="sendTestNotification" class="my-2">{{
            $t("app.user.profile.pushRegistrations.sendTestNotification")
          }}</b-button>
        </div>
      </div>
    </div>

    <div class="alert alert-danger" role="alert" v-if="errorMessage">
      {{ errorMessage }}
    </div>

    <b-table
      ref="table"
      id="user-push-registration-table"
      :fields="fields"
      :items="loadTableData"
      :current-page="currentPage"
      :per-page="perPage"
      primary-key="id"
      outlined
      responsive
      thead-class="d-none"
      show-empty
      :empty-text="$t('shared.emptyData')"
    >
      <template #cell(device)="data">
        <span
          :class="{ 'font-weight-bold': data.item.id == pushRegistrationId }"
          >{{ data.item.device }}</span
        >
      </template>
      <template #cell(actions)="data">
        <b-button
          @click="confirmDeletePushRegistration(data.item.id)"
          class="remove-push-registration-btn"
          variant="light"
          ><b-icon icon="x"></b-icon
        ></b-button>
      </template>
    </b-table>
    <b-pagination
      v-if="totalRows > perPage"
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      aria-controls="user-push-registration-table"
    ></b-pagination>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      errorMessage: null,
      fields: [
        {
          key: "device",
          tdClass: "align-middle",
        },
        {
          key: "platform",
          tdClass: "align-middle text-capitalize",
        },
        {
          key: "actions",
          tdClass: "text-right align-middle",
        },
      ],
      totalRows: 0,
      currentPage: 1,
      perPage: 10,
      searchResult: {
        items: [],
      },
    };
  },
  computed: {
    notificationsSupported() {
      return this.$store.state.notifications.notificationsSupported;
    },
    notificationPermission() {
      return this.$store.state.notifications.notificationPermission;
    },
    /* istanbul ignore next */
    pushRegistrationId() {
      return this.$store.state.notifications.pushRegistrationId;
    },
  },
  watch: {
    /* istanbul ignore next */
    "$store.state.notifications.pushRegistrationId": function () {
      this.refreshTableData();
    },
  },
  methods: {
    /* istanbul ignore next */
    registerPush() {
      this.$store.dispatch("notifications/registerPush").then(
        () => {
          this.$root.makeSuccessToast(
            this.$t("app.user.profile.pushRegistrations.addedMessage")
          );
        },
        (error) => {
          this.$root.makeErrorToast(error.message);
        }
      );
    },
    /* istanbul ignore next */
    unregisterPush() {
      this.$store.dispatch("notifications/unregisterPush").then(
        () => {
          this.$root.makeSuccessToast(
            this.$t("app.user.profile.pushRegistrations.deletedMessage")
          );
          this.refreshTableData();
        },
        (error) => {
          this.$root.makeErrorToast(error.message);
        }
      );
    },
    /* istanbul ignore next */
    sendTestNotification() {
      this.$store.dispatch("notifications/sendTestNotification");
    },
    loadTableData(ctx, callback) {
      const vm = this;
      axios
        .get(`/api/user/push-registrations`, {
          params: {
            page: ctx.currentPage,
            per_page: ctx.perPage,
          },
          handleRequestStart: () => (this.errorMessage = null),
          handleRequestError: /* istanbul ignore next */ (
            _error,
            message
          ) => /* istanbul ignore next */ {
            this.errorMessage = message;
            callback([]);
          },
        })
        .then((response) => {
          vm.totalRows = response.data.total;
          callback(response.data.items);
        });
      return null;
    },
    /* istanbul ignore next */
    refreshTableData() {
      this.$refs.table.refresh();
    },
    /* istanbul ignore next */
    confirmDeletePushRegistration(pushRegistrationId) {
      if (
        confirm(
          this.$t("app.user.profile.pushRegistrations.deleteConfirmation")
        )
      ) {
        this.deletePushRegistration(pushRegistrationId);
      }
    },
    /* istanbul ignore next */
    deletePushRegistration(pushRegistrationId) {
      this.$store
        .dispatch("notifications/deletePushRegistration", {
          pushRegistrationId: pushRegistrationId,
        })
        .then(
          () => {
            this.$root.makeSuccessToast(
              this.$t("app.user.profile.pushRegistrations.deletedMessage")
            );
            this.refreshTableData();
          },
          (error) => {
            this.$root.makeErrorToast(error.message);
          }
        );
    },
  },
};
</script>
