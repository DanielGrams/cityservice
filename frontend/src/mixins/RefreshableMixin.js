export default {
  data() {
    return {
      dataFetchedAt: null,
    };
  },
  watch: {
    /* istanbul ignore next */
    "$store.state.appIsActive"(appIsActive) /* istanbul ignore next */ {
      /* istanbul ignore next */
      if (appIsActive && this.dataFetchedAt != null) {
        const now = new Date();
        const diffInMs = now.getTime() - this.dataFetchedAt.getTime();
        const diffInSec = diffInMs / 1000;

        if (diffInSec >= 60) {
          this.refreshData();
        }
      }
    },
  },
  methods: {
    onRefreshingDataStarted() {
      this.dataFetchedAt = new Date();
    },
    /* istanbul ignore next */
    refreshData() {
      // overwrite
    }
  }
};
