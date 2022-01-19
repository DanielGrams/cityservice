import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import moment from 'moment'
import VueMoment from 'vue-moment';

import './custom.scss'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

require('moment/locale/de');
moment.locale('de');
Vue.use(VueMoment, { moment });

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
