import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import moment from 'moment'
import VueMoment from 'vue-moment';
import VueMeta from 'vue-meta'

import './custom.scss'
import i18n from './i18n'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

require('moment/locale/de');
moment.locale('de');
Vue.use(VueMoment, { moment });

Vue.use(VueMeta, {
  refreshOnceOnNavigation: true
})

new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount('#app')
