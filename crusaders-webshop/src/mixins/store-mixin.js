export const storeMixin = {
  computed: {
    adminIsAuthenticated() {
      return this.$store.getters.adminIsAuthenticated;
    }
  },
  methods: {
    userIsAuthenticated(userId) {
      return this.$store.getters.userIsAuthenticated(userId);
    }
  }
};
