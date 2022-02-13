export default {
  props: {
    model: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      innerModel: {},
    };
  },
  created() {
    this.innerModel = this.model;
  },
};
