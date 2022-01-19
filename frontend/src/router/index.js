import Vue from 'vue'
import VueRouter from 'vue-router'
import News from '../views/News.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/news',
    name: 'News',
    component: News
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
