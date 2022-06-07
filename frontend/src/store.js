import Vue from 'vue'
import Vuex from 'vuex'

import { auth } from './app/auth/store';
import { notifications } from './app/notifications/store';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    appIsActive: true,
  },
  mutations: {
    /* istanbul ignore next */
    setAppIsActive (state, isActive) {
      state.appIsActive = isActive;
    }
  },
  actions: {
  },
  modules: {
    auth,
    notifications
  }
})
