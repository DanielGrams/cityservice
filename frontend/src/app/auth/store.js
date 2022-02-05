import AuthService from "../../services/auth.service";

export const auth = {
  namespaced: true,
  state: {
    status: {
      initialized: false,
      initializing: false,
      loggingIn: false,
      loggingOut: false,
      loggedIn: false,
    },
    user: null,
  },
  getters: {
    isAuthenticated: (state) => {
      return state.status.loggedIn;
    },
    isAdmin: (state, getters) => {
      return (
        getters.isAuthenticated &&
        state.user &&
        state.user.roles &&
        state.user.roles.includes("admin")
      );
    },
  },
  actions: {
    init({ commit }) {
      commit("initStart");
      return AuthService.init().then(
        (user) => {
          commit("initSuccess", user);
          return Promise.resolve(user);
        },
        (error) => {
          commit("initFailure");
          return Promise.reject(error);
        }
      );
    },
    login({ commit }, { email, password }) {
      commit("loginStart");
      return AuthService.login(email, password).then(
        (user) => {
          commit("loginSuccess", user);
          return Promise.resolve(user);
        },
        (error) => {
          commit("loginFailure");
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      commit("logoutStart");
      return AuthService.logout().then(
        () => {
          commit("logoutSuccess");
          return Promise.resolve();
        },
        /* istanbul ignore next */
        (error) => {
          commit("logoutFailure");
          return Promise.reject(error);
        }
      );
    },
  },
  mutations: {
    initStart(state) {
      state.status.initializing = true;
    },
    initSuccess(state, user) {
      state.status.initializing = false;
      state.status.initialized = true;
      state.status.loggedIn = true;
      state.user = user;
    },
    initFailure(state) {
      state.status.initializing = false;
      state.status.initialized = true;
      state.status.loggedIn = false;
      state.user = null;
    },
    loginStart(state) {
      state.status.loggingIn = true;
    },
    loginSuccess(state, user) {
      state.status.loggingIn = false;
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggingIn = false;
      state.status.loggedIn = false;
      state.user = null;
    },
    logoutStart(state) {
      state.status.loggingOut = true;
    },
    logoutSuccess(state) {
      state.status.loggingOut = false;
      state.status.loggedIn = false;
      state.user = null;
    },
    /* istanbul ignore next */
    logoutFailure(state) {
      state.status.loggingOut = false;
    },
  },
};
