<template>
  <div>
    <h4>{{ $t("app.user.profile.notifications.title") }}</h4>
    <div v-if="!notificationsSupported">
      {{ $t("app.user.profile.notifications.notSupported") }}
    </div>
    <div v-if="notificationsSupported">
      <div v-if="notificationPermission == 'denied'">
        {{ $t("app.user.profile.notifications.permissionDenied") }}
      </div>
      <div v-if="notificationPermission != 'denied'">
        <div v-if="!pushToken">
          <div>{{ $t("app.user.profile.notifications.notRegistered") }}</div>
          <b-button @click="registerPush" class="my-2">{{
            $t("app.user.profile.notifications.registerPush")
          }}</b-button>
        </div>
        <div v-if="pushToken">
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
      notificationsSupported: false,
      notificationPermission: null, // "default" | "denied" | "granted"
      pushToken: null,
      pushRegistrationId: null,
      errorMessage: null,
      fields: [
        {
          key: "device",
          tdClass: "align-middle",
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
  created() {
    this.initializePush();
  },
  methods: {
    initializePush() {
      this.notificationsSupported =
        "Notification" in window &&
        "PushManager" in window &&
        navigator.serviceWorker != null;
      this.notificationPermission = Notification.permission;

      /* istanbul ignore next */
      if (
        this.notificationsSupported &&
        this.notificationPermission == "granted"
      ) {
        this.loadPushRegistration();
      }
    },
    /* istanbul ignore next */
    loadPushRegistration() {
      navigator.serviceWorker.ready.then((reg) => {
        if (reg.pushManager == null) {
          return;
        }

        reg.pushManager
          .getSubscription()
          .then((subscription) => {
            if (subscription == null) {
              this.pushToken = null;
              this.pushRegistrationId = null;
            }

            const token = JSON.stringify(subscription);
            axios
              .get(
                `/api/user/push-registrations?token=${encodeURIComponent(
                  token
                )}`
              )
              .then((response) => {
                if (response.data.items.length > 0) {
                  this.pushToken = token;
                  this.pushRegistrationId = response.data.items[0].id;
                } else {
                  this.pushToken = null;
                  this.pushRegistrationId = null;
                }
              })
              .catch(() => {
                this.pushToken = null;
                this.pushRegistrationId = null;
              });
          })
          .catch((e) => {
            this.$root.makeErrorToast(e.message);
          });
      });
    },
    /* istanbul ignore next */
    registerPush() {
      Notification.requestPermission(() => {
        this.notificationPermission = Notification.permission;

        if (this.notificationPermission != "granted") {
          return;
        }

        navigator.serviceWorker.ready.then((reg) => {
          if (reg.pushManager == null) {
            this.$root.makeErrorToast(
              this.$t("app.user.profile.notifications.notSupported")
            );
            return;
          }

          reg.pushManager
            .subscribe({
              userVisibleOnly: true,
              applicationServerKey: process.env.VUE_APP_VAPID_SERVER_KEY,
            })
            .then((subscription) => {
              const token = JSON.stringify(subscription);
              const post = {
                device: window.navigator.userAgent,
                platform: "web",
                token: token,
              };
              axios
                .post("/api/user/push-registrations", post)
                .then((response) => {
                  this.pushToken = token;
                  this.$root.makeSuccessToast(
                    this.$t("app.user.profile.pushRegistrations.addedMessage")
                  );
                  this.refreshTableData();

                  if (response.status == 201) {
                    this.pushRegistrationId = response.data.id;
                  }
                });
            })
            .catch((e) => {
              this.$root.makeErrorToast(e.message);
            });
        });
      });
    },
    /* istanbul ignore next */
    unregisterPush() {
      this.deletePushRegistration(this.pushRegistrationId);

      navigator.serviceWorker.ready.then((reg) => {
        reg.pushManager
          .getSubscription()
          .then((subscription) => {
            if (subscription != null) {
              subscription.unsubscribe();
            }
          })
          .catch((e) => {
            this.$root.makeErrorToast(e.message);
          });
      });
    },
    /* istanbul ignore next */
    sendTestNotification() {
      axios.post(
        `/api/user/push-registrations/${this.pushRegistrationId}/send`
      );
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
      axios
        .delete(`/api/user/push-registrations/${pushRegistrationId}`)
        .then(() => {
          this.$root.makeSuccessToast(
            this.$t("app.user.profile.pushRegistrations.deletedMessage")
          );
          this.refreshTableData();

          if (pushRegistrationId == this.pushRegistrationId) {
            this.pushRegistrationId = null;
            this.pushToken = null;
          }
        });
    },
  },
};
</script>
