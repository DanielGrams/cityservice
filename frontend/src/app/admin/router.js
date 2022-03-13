const Module = () => import("./Module.vue");
const Home = () => import("./views/Home.vue");
import newsFeedsRoutes from "./news-feeds/router";
import placesRoutes from "./places/router";

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
      ...placesRoutes,
    ],
  },
];

export default routes;
