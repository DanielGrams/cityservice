const Module = () => import("./Module.vue");
const List = () => import("./views/List.vue");

const routes = [
  {
    path: "places",
    component: Module,
    children: [
      {
        path: "/",
        component: List,
      },
    ],
  },
];

export default routes;
