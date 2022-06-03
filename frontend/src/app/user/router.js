const Module = () => import("./Module.vue");
import homeRoutes from "./home/router";
import profileRoutes from "./profile/router";
import placesRoutes from "./places/router";
import recyclingStreetsRoutes from "./recycling-streets/router";

const routes = [
  {
    path: "/user",
    component: Module,
    meta: {
      requiresAuth: true,
    },
    children: [
      ...homeRoutes,
      ...profileRoutes,
      ...placesRoutes,
      ...recyclingStreetsRoutes,
    ],
  },
];

export default routes;
