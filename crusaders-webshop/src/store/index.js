import { createStore } from 'vuex';

export default createStore({
  state: {
    adminIsAuthenticated: false,
    currentUser: {
      userIsAuthenticated: false,
      userId: null
    }
  },
  mutations: {
    setAdminAuthentication(state, status) {
      state.adminIsAuthenticated = status;
    },
    setUserAuthentication(state, user) {
      state.currentUser.userIsAuthenticated = user.isAuthenticated;
      state.currentUser.userId = user.userId;
    }
  },
  actions: {
    async loginAdmin({ commit }) {
      commit('setAdminAuthentication', true);
    },
    async logoutAdmin({ commit }) {
      commit('setAdminAuthentication', false);
    },
    async loginUser({ commit }, userId) {
      commit('setUserAuthentication', { isAuthenticated: true, userId });
    },
    async logoutUser({ commit }, userId) {
      commit('setUserAuthentication', { isAuthenticated: false, userId });
    }
  },
  getters: {
    adminIsAuthenticated: (state) => state.adminIsAuthenticated,
    userIsAuthenticated: (state) => (userId) => {
      const userIdAsString = JSON.stringify(state.currentUser.userId);
      return userIdAsString === userId && state.currentUser.userIsAuthenticated;
    }
  }
});
