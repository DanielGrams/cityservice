import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";
import placesRoutes from "./places/router";
import recyclingStreetsRoutes from "./recycling-streets/router";
import adminRoutes from "./admin/router";
import userRoutes from "./user/router";
import authRoutes from "./auth/router";
import rootRoutes from "./root/router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: () => import("./root/views/Home.vue"),
  },
  ...authRoutes,
  ...placesRoutes,
  ...recyclingStreetsRoutes,
  ...userRoutes,
  ...adminRoutes,
  ...rootRoutes,
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
    return next({ path: "/login", query: { redirectTo: to.fullPath } });
  }

  if (
    to.matched.some((record) => record.meta.requiresAdmin) &&
    !store.getters["auth/isAdmin"]
  ) {
    return next("/user/profile");
  }

  if (
    to.matched.some((record) => record.meta.requiresAnonymous) &&
    store.state.auth.status.loggedIn
  ) {
    return next("/user/profile");
  }

  next();
});

export default router;
