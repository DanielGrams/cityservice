import Vue from "vue";
import VueRouter from "vue-router";
import News from "../views/News.vue";
import Login from "../views/Login.vue";
import store from "../store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: News,
  },
  {
    path: "/news",
    name: "News",
    component: News,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      requiresAnonymous: true,
    },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("../views/Profile.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/admin",
    name: "Admin",
    component: () => import("../views/Admin.vue"),
    meta: {
      requiresAdmin: true,
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (store.state.auth.status.initialized) {
    return next();
  }

  store.dispatch("auth/init").then(
    () => {
      next();
    },
    () => {
      next();
    }
  );
});

router.beforeEach((to, from, next) => {
  if (
    to.matched.some(
      (record) => record.meta.requiresAuth || record.meta.requiresAdmin
    ) &&
    !store.state.auth.status.loggedIn
  ) {
    return next({ name: "Login", query: { redirectTo: to.fullPath } });
  }

  if (
    to.matched.some((record) => record.meta.requiresAdmin) &&
    !store.getters["auth/isAdmin"]
  ) {
    return next({ name: "Profile" });
  }

  if (
    to.matched.some((record) => record.meta.requiresAnonymous) &&
    store.state.auth.status.loggedIn
  ) {
    return next({ name: "Profile" });
  }

  next();
});

export default router;
