const Module = () => import("./Module.vue");
const Read = () => import("./views/Read.vue");

const routes = [
  {
    path: "/recycling-streets",
    component: Module,
    children: [
      {
        path: ":id",
        component: Read,
      },
    ],
  },
];

export default routes;
