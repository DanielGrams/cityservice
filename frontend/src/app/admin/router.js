const Module = () => import("./Module.vue");
const Home = () => import("./views/Home.vue");
import newsFeedsRoutes from "./news-feeds/router";

const routes = [
  {
    path: "/admin",
    component: Module,
    meta: {
      requiresAdmin: true,
    },
    children: [
      {
        path: "/",
        component: Home,
      },
      ...newsFeedsRoutes,
    ],
  },
];

export default routes;
